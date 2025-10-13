"""
批量上架草稿商品脚本
用法：python activate_draft_products.py
"""
from app.database import SessionLocal
from app.models.product import Product
from app.core.enums_v2 import ProductStatus, AuditStatus

def activate_all_draft_products():
    """将所有DRAFT状态的商品改为ACTIVE"""
    db = SessionLocal()

    try:
        # 查找所有DRAFT状态的商品
        draft_products = db.query(Product).filter(
            Product.status == ProductStatus.DRAFT,
            Product.is_deleted == False
        ).all()

        if not draft_products:
            print("没有找到草稿商品")
            return

        print(f"找到 {len(draft_products)} 个草稿商品")

        for product in draft_products:
            print(f"上架商品: ID={product.id}, 名称={product.name}")
            product.status = ProductStatus.ACTIVE
            product.audit_status = AuditStatus.APPROVED

        db.commit()
        print(f"成功上架 {len(draft_products)} 个商品！")

    except Exception as e:
        db.rollback()
        print(f"上架失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    activate_all_draft_products()
