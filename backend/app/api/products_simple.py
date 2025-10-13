"""
简化版商品API - 去除过度抽象的服务层
直接在API层处理业务逻辑，保持简洁
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.core.enums_v2 import ProductStatus, ProductCategory, AuditStatus
from app.core.permissions import get_current_user, require_admin_role

router = APIRouter(prefix="/products-simple", tags=["products-simple"])


@router.post("/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建商品 - 简化版"""

    # 基础权限检查（保留必要的权限控制）
    if current_user.role not in ["ADMIN", "SUPER_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以创建商品"
        )

    # 创建商品
    product = Product(
        name=product_data.name,
        description=product_data.description,
        category=product_data.category,
        price=product_data.price,
        stock_quantity=product_data.stock_quantity or 0,
        images=product_data.images or [],
        usage_instructions=product_data.usage_instructions or "",
        is_featured=product_data.is_featured,
        is_common=product_data.is_common,
        status=ProductStatus.DRAFT,  # 新创建的商品默认为草稿状态
        audit_status=AuditStatus.PENDING,
        created_by=current_user.id
    )

    try:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建商品失败: {str(e)}"
        )


@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[ProductCategory] = None,
    status: Optional[ProductStatus] = None,
    db: Session = Depends(get_db)
):
    """获取商品列表 - 简化版"""

    query = db.query(Product).filter(Product.is_deleted == False)

    # 简单过滤
    if category:
        query = query.filter(Product.category == category)
    if status:
        query = query.filter(Product.status == status)

    # 只显示审核通过的商品（给普通用户）
    # 管理员可以看到所有商品
    # 这里为了简化，暂时显示所有状态的商品

    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """获取单个商品 - 简化版"""

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在"
        )

    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新商品 - 简化版"""

    # 权限检查
    if current_user.role not in ["ADMIN", "SUPER_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以更新商品"
        )

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在"
        )

    # 更新字段
    update_data = product_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(product, field):
            setattr(product, field, value)

    product.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新商品失败: {str(e)}"
        )


@router.patch("/{product_id}/status")
def change_product_status(
    product_id: int,
    new_status: ProductStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role)
):
    """修改商品状态 - 简化版"""

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在"
        )

    # 简单的状态验证（去除复杂的状态机）
    if new_status == ProductStatus.ACTIVE and product.stock_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="库存不足，无法上架"
        )

    product.status = new_status
    product.updated_at = datetime.utcnow()

    try:
        db.commit()
        return {"message": f"商品状态已更新为 {new_status}", "status": new_status}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"状态更新失败: {str(e)}"
        )


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_role)
):
    """删除商品（软删除）- 简化版"""

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在"
        )

    # 软删除
    product.is_deleted = True
    product.updated_at = datetime.utcnow()

    try:
        db.commit()
        return {"message": "商品已删除"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败: {str(e)}"
        )