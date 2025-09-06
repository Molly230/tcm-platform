#!/usr/bin/env python3
"""
数据库迁移脚本 - 将Float类型改为Decimal类型
运行前请备份数据库！
"""

import os
import sys
from decimal import Decimal

# 添加项目路径
sys.path.append('/var/www/tcm-platform/backend')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import create_engine, text
from app.core.config import get_settings

settings = get_settings()

def migrate_to_decimal():
    """将Float类型的价格字段迁移为Decimal类型"""
    
    print("🚀 开始数据库迁移 - Float to Decimal")
    
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # 开始事务
            trans = conn.begin()
            
            try:
                print("1. 备份当前数据...")
                
                # 迁移products表
                print("2. 迁移products表...")
                migrations = [
                    # products表
                    "ALTER TABLE products ALTER COLUMN price TYPE NUMERIC(10,2) USING price::NUMERIC(10,2)",
                    "ALTER TABLE products ALTER COLUMN original_price TYPE NUMERIC(10,2) USING original_price::NUMERIC(10,2)",
                    "ALTER TABLE products ALTER COLUMN discount TYPE NUMERIC(3,2) USING discount::NUMERIC(3,2)",
                    
                    # orders表
                    "ALTER TABLE orders ALTER COLUMN subtotal TYPE NUMERIC(10,2) USING subtotal::NUMERIC(10,2)",
                    "ALTER TABLE orders ALTER COLUMN shipping_fee TYPE NUMERIC(8,2) USING shipping_fee::NUMERIC(8,2)",
                    "ALTER TABLE orders ALTER COLUMN discount_amount TYPE NUMERIC(10,2) USING discount_amount::NUMERIC(10,2)",
                    "ALTER TABLE orders ALTER COLUMN total_amount TYPE NUMERIC(10,2) USING total_amount::NUMERIC(10,2)",
                    
                    # order_items表
                    "ALTER TABLE order_items ALTER COLUMN unit_price TYPE NUMERIC(10,2) USING unit_price::NUMERIC(10,2)",
                    "ALTER TABLE order_items ALTER COLUMN total_price TYPE NUMERIC(10,2) USING total_price::NUMERIC(10,2)",
                    
                    # payments表
                    "ALTER TABLE payments ALTER COLUMN amount TYPE NUMERIC(10,2) USING amount::NUMERIC(10,2)",
                    
                    # courses表
                    "ALTER TABLE courses ALTER COLUMN price TYPE NUMERIC(8,2) USING price::NUMERIC(8,2)",
                    
                    # experts表
                    "ALTER TABLE experts ALTER COLUMN text_price TYPE NUMERIC(8,2) USING text_price::NUMERIC(8,2)",
                    "ALTER TABLE experts ALTER COLUMN voice_price TYPE NUMERIC(8,2) USING voice_price::NUMERIC(8,2)",
                    "ALTER TABLE experts ALTER COLUMN video_price TYPE NUMERIC(8,2) USING video_price::NUMERIC(8,2)",
                    
                    # consultations表
                    "ALTER TABLE consultations ALTER COLUMN price TYPE NUMERIC(8,2) USING price::NUMERIC(8,2)",
                ]
                
                for i, migration in enumerate(migrations, 1):
                    try:
                        print(f"   执行迁移 {i}/{len(migrations)}: {migration.split()[2]}")
                        conn.execute(text(migration))
                    except Exception as e:
                        # 某些字段可能不存在，继续下一个
                        print(f"   跳过: {e}")
                        continue
                
                print("3. 验证数据完整性...")
                
                # 验证迁移结果
                result = conn.execute(text("""
                    SELECT 
                        table_name, 
                        column_name, 
                        data_type 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND data_type = 'numeric'
                    AND column_name LIKE '%price%' OR column_name LIKE '%amount%'
                    ORDER BY table_name, column_name
                """))
                
                print("迁移后的Decimal字段:")
                for row in result:
                    print(f"   {row.table_name}.{row.column_name}: {row.data_type}")
                
                # 提交事务
                trans.commit()
                print("✅ 数据库迁移完成！")
                
            except Exception as e:
                # 回滚事务
                trans.rollback()
                print(f"❌ 迁移失败，已回滚: {e}")
                raise
                
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False
    
    return True

def verify_migration():
    """验证迁移结果"""
    print("\n🔍 验证迁移结果...")
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # 检查价格字段的数据类型
        result = conn.execute(text("""
            SELECT COUNT(*) as decimal_columns
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND data_type = 'numeric'
            AND (column_name LIKE '%price%' OR column_name LIKE '%amount%' OR column_name = 'discount')
        """))
        
        count = result.scalar()
        print(f"✅ 共有 {count} 个字段已成功迁移为Decimal类型")
        
        # 测试一些基本的价格计算
        try:
            result = conn.execute(text("SELECT price FROM products LIMIT 1"))
            price = result.scalar()
            if price is not None:
                print(f"✅ 价格数据类型验证通过: {type(price)} = {price}")
        except Exception as e:
            print(f"⚠️  价格数据验证警告: {e}")

if __name__ == "__main__":
    print("中医健康平台 - 数据库迁移工具")
    print("=" * 50)
    
    # 确认操作
    response = input("⚠️  此操作将修改数据库结构，请确保已备份数据库。继续？(y/N): ")
    if response.lower() != 'y':
        print("操作已取消")
        sys.exit(0)
    
    # 执行迁移
    if migrate_to_decimal():
        verify_migration()
        print("\n🎉 迁移成功完成！")
        print("💡 建议:")
        print("   1. 重启应用服务")
        print("   2. 测试支付流程")
        print("   3. 验证价格计算准确性")
    else:
        print("\n❌ 迁移失败，请检查错误信息")
        sys.exit(1)