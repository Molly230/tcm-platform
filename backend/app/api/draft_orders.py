"""
预订单API - 安全的checkout流程
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime, timedelta
import uuid

from app.database import get_db
from app import models
from app.core.permissions import get_current_user
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/draft-orders", tags=["预订单"])

# 强制重载标记 - 修改时间戳

class DraftOrderItem(BaseModel):
    product_id: int
    quantity: int

class CreateDraftOrderRequest(BaseModel):
    items: List[DraftOrderItem]
    from_source: str = "cart"  # cart, direct_buy, etc.

class DraftOrderResponse(BaseModel):
    draft_order_id: str
    expires_at: datetime
    total_amount: float
    items_count: int

class DraftOrderDetailResponse(BaseModel):
    draft_order_id: str
    items: List[dict]
    total_amount: float
    subtotal: float
    expires_at: datetime
    is_expired: bool

@router.post("/create", response_model=DraftOrderResponse)
async def create_draft_order(
    request: CreateDraftOrderRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """创建预订单"""
    try:
        # 验证商品存在性和库存
        draft_items = []
        total_amount = 0
        
        for item in request.items:
            product = db.query(models.Product).filter(
                models.Product.id == item.product_id,
                models.Product.is_deleted == False
            ).first()
            
            if not product:
                raise HTTPException(status_code=404, detail=f"商品 {item.product_id} 不存在")
            
            if product.stock_quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"商品 {product.name} 库存不足")
            
            item_total = float(product.price) * item.quantity
            total_amount += item_total
            
            draft_items.append({
                "product_id": product.id,
                "product_name": product.name,
                "product_price": float(product.price),
                "quantity": item.quantity,
                "subtotal": item_total,
                "product_image": product.images[0] if product.images else None,
                "product_description": product.description
            })
        
        # 生成预订单ID
        draft_order_id = f"DRAFT_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
        
        # 设置过期时间（30分钟）
        expires_at = datetime.now() + timedelta(minutes=30)
        
        # 创建预订单记录（存储在临时表或缓存中）
        draft_order = models.DraftOrder(
            id=draft_order_id,
            user_id=current_user.id,
            items_json=draft_items,  # 存储JSON格式的商品信息
            total_amount=total_amount,
            expires_at=expires_at,
            from_source=request.from_source,
            created_at=datetime.now()
        )
        
        db.add(draft_order)
        db.commit()
        
        logger.info(f"Created draft order: {draft_order_id} for user {current_user.id}")
        
        return DraftOrderResponse(
            draft_order_id=draft_order_id,
            expires_at=expires_at,
            total_amount=total_amount,
            items_count=len(draft_items)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create draft order failed: {e}")
        raise HTTPException(status_code=500, detail="创建预订单失败")

@router.get("/{draft_order_id}", response_model=DraftOrderDetailResponse)
async def get_draft_order(
    draft_order_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """获取预订单详情"""
    try:
        # 查找预订单
        draft_order = db.query(models.DraftOrder).filter(
            models.DraftOrder.id == draft_order_id,
            models.DraftOrder.user_id == current_user.id
        ).first()
        
        if not draft_order:
            raise HTTPException(status_code=404, detail="预订单不存在")
        
        # 检查是否过期
        is_expired = datetime.now() > draft_order.expires_at
        
        if is_expired:
            raise HTTPException(status_code=410, detail="预订单已过期")
        
        # 重新验证商品价格（防止价格变动）
        current_items = []
        current_total = 0
        
        for item in draft_order.items_json:
            product = db.query(models.Product).filter(
                models.Product.id == item["product_id"],
                models.Product.is_deleted == False
            ).first()
            
            if not product:
                continue  # 商品可能已下架
            
            # 使用当前价格
            current_price = float(product.price)
            current_subtotal = current_price * item["quantity"]
            current_total += current_subtotal
            
            current_items.append({
                **item,
                "current_price": current_price,
                "current_subtotal": current_subtotal,
                "price_changed": current_price != item["product_price"]
            })
        
        return DraftOrderDetailResponse(
            draft_order_id=draft_order_id,
            items=current_items,
            total_amount=current_total,
            subtotal=current_total,  # 暂不考虑优惠券
            expires_at=draft_order.expires_at,
            is_expired=is_expired
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get draft order failed: {e}")
        raise HTTPException(status_code=500, detail="获取预订单失败")

@router.post("/{draft_order_id}/convert")
async def convert_draft_to_order(
    draft_order_id: str,
    customer_info: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """将预订单转换为正式订单"""
    try:
        # 获取预订单
        draft_order = db.query(models.DraftOrder).filter(
            models.DraftOrder.id == draft_order_id,
            models.DraftOrder.user_id == current_user.id
        ).first()
        
        if not draft_order:
            raise HTTPException(status_code=404, detail="预订单不存在")
        
        if datetime.now() > draft_order.expires_at:
            raise HTTPException(status_code=410, detail="预订单已过期")
        
        # 创建正式订单
        order_number = f"TCM{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"
        
        order = models.Order(
            order_number=order_number,
            user_id=current_user.id,
            total_amount=draft_order.total_amount,
            status="pending_payment",
            customer_info=customer_info,
            created_at=datetime.now()
        )
        
        db.add(order)
        db.flush()  # 获取order.id
        
        # 创建订单项
        for item in draft_order.items_json:
            order_item = models.OrderItem(
                order_id=order.id,
                product_id=item["product_id"],
                product_name=item["product_name"],
                product_price=item["product_price"],
                quantity=item["quantity"],
                subtotal=item["subtotal"]
            )
            db.add(order_item)
        
        # 删除预订单
        db.delete(draft_order)
        
        db.commit()
        
        logger.info(f"Converted draft order {draft_order_id} to order {order_number}")
        
        return {
            "success": True,
            "order_number": order_number,
            "order_id": order.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Convert draft order failed: {e}")
        raise HTTPException(status_code=500, detail="创建订单失败")

@router.delete("/{draft_order_id}")
async def cancel_draft_order(
    draft_order_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """取消预订单"""
    try:
        draft_order = db.query(models.DraftOrder).filter(
            models.DraftOrder.id == draft_order_id,
            models.DraftOrder.user_id == current_user.id
        ).first()
        
        if not draft_order:
            raise HTTPException(status_code=404, detail="预订单不存在")
        
        db.delete(draft_order)
        db.commit()
        
        return {"success": True, "message": "预订单已取消"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Cancel draft order failed: {e}")
        raise HTTPException(status_code=500, detail="取消预订单失败")