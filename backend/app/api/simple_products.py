"""
简洁的商品API
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

from app.database import get_db
from app.models.simple_product import SimpleProduct, SimpleCart, SimpleOrder, SimpleOrderItem

router = APIRouter(prefix="/api/simple", tags=["simple"])

# Pydantic模型
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    category: Optional[str] = None
    images: Optional[List[str]] = None
    stock: int = 0

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    original_price: Optional[float]
    category: Optional[str]
    images: Optional[List[str]]
    stock: int
    is_active: bool
    created_at: datetime

class CartItem(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    shipping_name: str
    shipping_phone: str
    shipping_address: str
    items: List[CartItem]

# 商品相关API
@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取商品列表"""
    query = db.query(SimpleProduct).filter(SimpleProduct.is_active == True)
    
    if category:
        query = query.filter(SimpleProduct.category == category)
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取商品详情"""
    product = db.query(SimpleProduct).filter(SimpleProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

@router.post("/products", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """创建商品"""
    db_product = SimpleProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 购物车相关API
@router.get("/cart/{user_id}")
async def get_cart(user_id: int, db: Session = Depends(get_db)):
    """获取购物车"""
    cart_items = db.query(SimpleCart).filter(SimpleCart.user_id == user_id).all()
    return cart_items

@router.post("/cart/{user_id}")
async def add_to_cart(user_id: int, item: CartItem, db: Session = Depends(get_db)):
    """添加到购物车"""
    # 检查商品是否存在
    product = db.query(SimpleProduct).filter(SimpleProduct.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    # 检查是否已在购物车中
    existing_item = db.query(SimpleCart).filter(
        SimpleCart.user_id == user_id,
        SimpleCart.product_id == item.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        cart_item = SimpleCart(
            user_id=user_id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    
    db.commit()
    return {"message": "已添加到购物车"}

@router.delete("/cart/{user_id}/{product_id}")
async def remove_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    """从购物车删除"""
    cart_item = db.query(SimpleCart).filter(
        SimpleCart.user_id == user_id,
        SimpleCart.product_id == product_id
    ).first()
    
    if cart_item:
        db.delete(cart_item)
        db.commit()
        return {"message": "已从购物车删除"}
    else:
        raise HTTPException(status_code=404, detail="购物车中没有此商品")

# 订单相关API
@router.post("/orders/{user_id}")
async def create_order(user_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    """创建订单"""
    # 生成订单号
    order_number = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
    
    # 计算总金额
    total_amount = 0
    order_items = []
    
    for item in order.items:
        product = db.query(SimpleProduct).filter(SimpleProduct.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"商品ID {item.product_id} 不存在")
        
        subtotal = float(product.price) * item.quantity
        total_amount += subtotal
        
        order_items.append({
            "product_id": item.product_id,
            "product_name": product.name,
            "product_price": float(product.price),
            "quantity": item.quantity,
            "subtotal": subtotal
        })
    
    # 创建订单
    db_order = SimpleOrder(
        order_number=order_number,
        user_id=user_id,
        total_amount=total_amount,
        shipping_name=order.shipping_name,
        shipping_phone=order.shipping_phone,
        shipping_address=order.shipping_address
    )
    db.add(db_order)
    db.flush()  # 获取订单ID
    
    # 创建订单项
    for item_data in order_items:
        order_item = SimpleOrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(order_item)
    
    # 清空购物车
    db.query(SimpleCart).filter(SimpleCart.user_id == user_id).delete()
    
    db.commit()
    db.refresh(db_order)
    
    return {
        "order_id": db_order.id,
        "order_number": db_order.order_number,
        "total_amount": float(db_order.total_amount),
        "status": db_order.status
    }

@router.get("/orders/{user_id}")
async def get_orders(user_id: int, db: Session = Depends(get_db)):
    """获取用户订单"""
    orders = db.query(SimpleOrder).filter(SimpleOrder.user_id == user_id).all()
    return orders

@router.get("/orders/{user_id}/{order_id}")
async def get_order(user_id: int, order_id: int, db: Session = Depends(get_db)):
    """获取订单详情"""
    order = db.query(SimpleOrder).filter(
        SimpleOrder.id == order_id,
        SimpleOrder.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 获取订单项
    order_items = db.query(SimpleOrderItem).filter(SimpleOrderItem.order_id == order_id).all()
    
    return {
        "order": order,
        "items": order_items
    }
