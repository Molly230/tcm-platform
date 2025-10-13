"""
购物车API - 完整的后端购物车实现
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal

from app.database import get_db
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse, CartItemResponse
from app.core.permissions import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])


def get_or_create_cart(user_id: int, db: Session) -> Cart:
    """获取或创建用户的购物车"""
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的购物车"""
    cart = get_or_create_cart(current_user.id, db)

    # 计算总价和总数量
    total_items = sum(item.quantity for item in cart.items)
    total_price = Decimal('0.00')

    # 组装商品信息
    items_with_products = []
    for item in cart.items:
        product = item.product
        if product and not product.is_deleted:
            # 使用当前价格计算（也可以用price_snapshot）
            current_price = Decimal(str(product.price))
            total_price += current_price * item.quantity

            # 直接构造字典，不经过Pydantic验证
            item_data = {
                'id': item.id,
                'cart_id': item.cart_id,
                'product_id': item.product_id,
                'quantity': item.quantity,
                'price_snapshot': float(item.price_snapshot) if item.price_snapshot else None,
                'created_at': item.created_at.isoformat(),
                'updated_at': item.updated_at.isoformat(),
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': str(product.price),
                    'images': product.images,
                    'stock_quantity': product.stock_quantity,
                    'category': product.category.value if hasattr(product.category, 'value') else str(product.category)
                }
            }
            items_with_products.append(item_data)

    # 直接返回字典，绕过Pydantic
    return {
        'id': cart.id,
        'user_id': cart.user_id,
        'items': items_with_products,
        'total_items': total_items,
        'total_price': str(total_price),
        'created_at': cart.created_at.isoformat(),
        'updated_at': cart.updated_at.isoformat()
    }


@router.post("/items")
def add_to_cart(
    item_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加商品到购物车"""

    # 检查商品是否存在
    product = db.query(Product).filter(
        Product.id == item_data.product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在"
        )

    # 检查库存
    if product.stock_quantity < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"库存不足，当前库存：{product.stock_quantity}"
        )

    # 获取或创建购物车
    cart = get_or_create_cart(current_user.id, db)

    # 检查商品是否已在购物车中
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_data.product_id
    ).first()

    if cart_item:
        # 更新数量
        new_quantity = cart_item.quantity + item_data.quantity
        if product.stock_quantity < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"库存不足，当前库存：{product.stock_quantity}，购物车已有：{cart_item.quantity}"
            )
        cart_item.quantity = new_quantity
    else:
        # 创建新的购物车项
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            price_snapshot=product.price
        )
        db.add(cart_item)

    try:
        db.commit()
        db.refresh(cart)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"��加到购物车失败: {str(e)}"
        )

    # 返回完整购物车
    return get_cart(db, current_user)


@router.put("/items/{item_id}")
def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新购物车商品数量"""

    cart = get_or_create_cart(current_user.id, db)

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="购物车项不存在"
        )

    if item_data.quantity == 0:
        # 删除
        db.delete(cart_item)
    else:
        # 检查库存
        product = cart_item.product
        if product.stock_quantity < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"库存不足，当前库存：{product.stock_quantity}"
            )
        cart_item.quantity = item_data.quantity

    try:
        db.commit()
        db.refresh(cart)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新购物车失败: {str(e)}"
        )

    return get_cart(db, current_user)


@router.delete("/items/{item_id}")
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """从购物车删除商品"""

    cart = get_or_create_cart(current_user.id, db)

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="购物车项不存在"
        )

    try:
        db.delete(cart_item)
        db.commit()
        db.refresh(cart)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败: {str(e)}"
        )

    return get_cart(db, current_user)


@router.delete("/clear", response_model=dict)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """清空购物车"""

    cart = get_or_create_cart(current_user.id, db)

    try:
        # 删除所有购物车项
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"清空购物车失败: {str(e)}"
        )

    return {"message": "购物车已清空"}
