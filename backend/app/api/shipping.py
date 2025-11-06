"""
配送管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.shipping import Shipping
from app.models.product import Order
from app.schemas.shipping import (
    ShippingCreate,
    ShippingUpdate,
    ShippingResponse,
    TrackingQueryRequest,
    TrackingQueryResponse
)
from app.services.kdniao_service import get_kdniao_service
from app.core.enums_v2 import ShippingStatus, OrderStatus, CourierCompany

router = APIRouter()


@router.post("/create", response_model=ShippingResponse)
async def create_shipping(
    shipping_data: ShippingCreate,
    db: Session = Depends(get_db)
):
    """
    创建配送记录（管理员发货时调用）
    """
    # 检查订单是否存在
    order = db.query(Order).filter(Order.id == shipping_data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    # 检查订单状态是否是已付款
    if order.status != OrderStatus.PAID:
        raise HTTPException(status_code=400, detail=f"订单状态不正确，当前状态: {order.status}")

    # 检查是否已经有配送记录
    existing = db.query(Shipping).filter(Shipping.order_id == shipping_data.order_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="该订单已有配送记录")

    # 验证快递公司代码
    try:
        CourierCompany(shipping_data.courier_company)
    except ValueError:
        raise HTTPException(status_code=400, detail="无效的快递公司代码")

    # 创建配送记录
    shipping = Shipping(
        order_id=shipping_data.order_id,
        courier_company=shipping_data.courier_company,
        courier_company_name=shipping_data.courier_company_name,
        tracking_number=shipping_data.tracking_number,
        courier_name=shipping_data.courier_name,
        courier_phone=shipping_data.courier_phone,
        status=ShippingStatus.SHIPPED,  # 创建时设为已发货
        shipped_at=datetime.now(),
        notes=shipping_data.notes,
        tracking_history=[]
    )

    db.add(shipping)

    # 更新订单状态为已发货
    order.status = OrderStatus.SHIPPED

    db.commit()
    db.refresh(shipping)

    return shipping


@router.get("/{shipping_id}", response_model=ShippingResponse)
def get_shipping(shipping_id: int, db: Session = Depends(get_db)):
    """获取配送记录详情"""
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="配送记录不存在")
    return shipping


@router.get("/order/{order_id}", response_model=ShippingResponse)
def get_shipping_by_order(order_id: int, db: Session = Depends(get_db)):
    """根据订单ID获取配送记录"""
    shipping = db.query(Shipping).filter(Shipping.order_id == order_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="该订单无配送记录")
    return shipping


@router.put("/{shipping_id}", response_model=ShippingResponse)
def update_shipping(
    shipping_id: int,
    shipping_update: ShippingUpdate,
    db: Session = Depends(get_db)
):
    """更新配送记录"""
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="配送记录不存在")

    # 更新字段
    update_data = shipping_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(shipping, field, value)

    db.commit()
    db.refresh(shipping)
    return shipping


@router.post("/track", response_model=TrackingQueryResponse)
async def track_shipment(
    request: TrackingQueryRequest,
    db: Session = Depends(get_db)
):
    """
    查询物流轨迹（调用快递鸟API）
    """
    # 获取配送记录
    shipping = db.query(Shipping).filter(Shipping.order_id == request.order_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="该订单无配送记录")

    try:
        # 调用快递鸟API查询
        kdniao = get_kdniao_service()
        result = await kdniao.track_shipment(
            courier_code=shipping.courier_company,
            tracking_number=shipping.tracking_number
        )

        if result["success"]:
            # 更新数据库中的物流轨迹
            shipping.tracking_history = result["tracking_history"]
            shipping.status = result["shipping_status"]

            # 如果已送达，更新送达时间和订单状态
            if result["shipping_status"] == "DELIVERED":
                if not shipping.delivered_at:
                    shipping.delivered_at = datetime.now()

                # 更新订单状态
                order = shipping.order
                if order:
                    order.status = OrderStatus.DELIVERED

            db.commit()

        return TrackingQueryResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询物流失败: {str(e)}")


@router.get("/list", response_model=List[ShippingResponse])
def list_shippings(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db)
):
    """获取配送记录列表（管理员）"""
    query = db.query(Shipping)

    if status:
        query = query.filter(Shipping.status == status)

    shippings = query.offset(skip).limit(limit).all()
    return shippings
