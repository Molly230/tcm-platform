"""
商品相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import schemas, models
from app.database import get_db
from datetime import datetime

router = APIRouter(tags=["products"])

@router.get("/", response_model=List[schemas.Product])
def get_products(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    search: Optional[str] = None,
    featured_only: bool = False,
    db: Session = Depends(get_db)
):
    """获取商品列表"""
    query = db.query(models.Product).filter(models.Product.status == "active")
    
    if category:
        query = query.filter(models.Product.category == category)
    
    if search:
        # 增强搜索：产品名称、功效特点、SEO关键词
        query = query.filter(
            (models.Product.name.contains(search)) |
            (models.Product.seo_keywords.contains(search)) |
            (models.Product.features.contains(search))
        )
    
    if featured_only:
        query = query.filter(models.Product.is_featured == True)
    
    # 按销量和评分排序
    query = query.order_by(models.Product.sales_count.desc(), models.Product.rating.desc())
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/common", response_model=List[schemas.Product])
def get_common_products(db: Session = Depends(get_db)):
    """获取常用产品列表"""
    products = db.query(models.Product).filter(
        models.Product.status == "active",
        models.Product.is_common == True
    ).order_by(models.Product.sales_count.desc()).all()
    return products

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取商品详情"""
    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.status == "active"
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """创建商品（管理员功能）"""
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    """更新商品信息（管理员功能）"""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # 更新商品信息
    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/categories/list")
def get_categories():
    """获取商品分类列表"""
    return [
        {"value": "中药材", "label": "中药材", "icon": "🌿"},
        {"value": "养生产品", "label": "养生产品", "icon": "💊"},
        {"value": "医疗器械", "label": "医疗器械", "icon": "🩺"},
        {"value": "保健食品", "label": "保健食品", "icon": "🍃"},
        {"value": "中医书籍", "label": "中医书籍", "icon": "📚"},
        {"value": "配套用品", "label": "配套用品", "icon": "🛠️"}
    ]

# 购物车相关API
@router.post("/cart/add")
def add_to_cart(
    product_id: int,
    quantity: int = 1,
    user_id: int = 1,  # 临时固定用户ID，实际应该从认证中获取
    db: Session = Depends(get_db)
):
    """添加商品到购物车"""
    # 检查商品是否存在
    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.status == "active"
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # 检查库存
    if product.stock_quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )
    
    # 检查是否已在购物车中
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == product_id
    ).first()
    
    if existing_item:
        # 更新数量
        existing_item.quantity += quantity
        if existing_item.quantity > product.stock_quantity:
            existing_item.quantity = product.stock_quantity
    else:
        # 新增购物车项
        cart_item = models.CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)
    
    db.commit()
    return {"message": "Added to cart successfully"}

@router.get("/cart/items", response_model=List[schemas.CartItem])
def get_cart_items(
    user_id: int = 1,  # 临时固定用户ID
    db: Session = Depends(get_db)
):
    """获取购物车商品"""
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id
    ).all()
    
    return cart_items

@router.put("/cart/update/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    """更新购物车商品数量"""
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    if quantity <= 0:
        # 删除商品
        db.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.commit()
    return {"message": "Cart updated successfully"}

@router.delete("/cart/remove/{item_id}")
def remove_cart_item(item_id: int, db: Session = Depends(get_db)):
    """从购物车移除商品"""
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

# 订单相关API
@router.post("/orders/create", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """创建订单"""
    import uuid
    from datetime import datetime
    
    # 生成订单号
    order_number = f"TCM{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:8].upper()}"
    
    db_order = models.Order(
        order_number=order_number,
        **order.dict()
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """获取订单详情"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order

@router.get("/orders/user/{user_id}", response_model=List[schemas.Order])
def get_user_orders(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取用户订单列表"""
    orders = db.query(models.Order).filter(
        models.Order.user_id == user_id
    ).order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()
    
    return orders

# 产品审核相关接口
@router.post("/submit", response_model=schemas.Product)
def submit_product(
    product: schemas.ProductSubmitRequest, 
    submitted_by: str,  # 实际应用中应该从JWT token获取
    db: Session = Depends(get_db)
):
    """提交产品等待审核"""
    product_data = product.dict()
    product_data["submitted_by"] = submitted_by
    product_data["audit_status"] = "pending"
    
    db_product = models.Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/pending", response_model=List[schemas.Product])
def get_pending_products(db: Session = Depends(get_db)):
    """获取待审核产品列表（管理员功能）"""
    products = db.query(models.Product).filter(
        models.Product.audit_status == "pending"
    ).order_by(models.Product.submitted_at.desc()).all()
    return products

@router.post("/{product_id}/audit")
def audit_product(
    product_id: int,
    audit_request: schemas.ProductAuditRequest,
    reviewer: str,  # 实际应用中应该从JWT token获取管理员信息
    db: Session = Depends(get_db)
):
    """审核产品（管理员功能）"""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # 更新审核状态
    if audit_request.action == "approve":
        db_product.audit_status = "approved"
        db_product.status = "active"  # 审核通过的产品设为在售
    elif audit_request.action == "reject":
        db_product.audit_status = "rejected"
        db_product.status = "inactive"  # 审核拒绝的产品设为下架
    elif audit_request.action == "revision":
        db_product.audit_status = "revision"
        db_product.status = "inactive"  # 需要修改的产品暂时下架
    
    db_product.reviewed_by = reviewer
    db_product.reviewed_at = datetime.utcnow()
    db_product.audit_notes = audit_request.notes
    
    db.commit()
    db.refresh(db_product)
    
    return {
        "message": f"产品审核{audit_request.action}成功",
        "product_id": product_id,
        "status": db_product.audit_status
    }