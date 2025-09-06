#!/usr/bin/env python3
"""
直接创建数据库表
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app import models

def create_tables():
    """创建所有数据库表"""
    print("Creating database tables...")
    
    # 删除所有现有表（如果存在）
    Base.metadata.drop_all(bind=engine)
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully!")
    
    # 显示创建的表
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Created tables: {tables}")

if __name__ == "__main__":
    create_tables()