#!/usr/bin/env python3
"""
简化版前后端字段一致性检查脚本
"""

import os
import re
from pathlib import Path

def check_backend_enums():
    """检查后端枚举值"""
    print("=== 后端枚举值检查 ===")
    
    backend_path = Path("backend/app")
    
    # 检查用户枚举
    user_model_path = backend_path / "models" / "user.py"
    user_schema_path = backend_path / "schemas" / "user.py"
    
    if user_model_path.exists():
        print("用户模型枚举值:")
        content = user_model_path.read_text(encoding='utf-8')
        user_roles = re.findall(r'(\w+)\s*=\s*"([^"]+)"', content)
        for role in user_roles:
            print(f"  {role[0]} = {role[1]}")
    
    # 检查课程枚举
    course_model_path = backend_path / "models" / "course.py"
    if course_model_path.exists():
        print("\n课程模型枚举值:")
        content = course_model_path.read_text(encoding='utf-8')
        categories = re.findall(r'(\w+)\s*=\s*"([^"]+)"', content)
        for cat in categories:
            print(f"  {cat[0]} = {cat[1]}")
    
    # 检查产品枚举
    product_model_path = backend_path / "models" / "product.py"
    if product_model_path.exists():
        print("\n产品模型枚举值:")
        content = product_model_path.read_text(encoding='utf-8')
        statuses = re.findall(r'(\w+)\s*=\s*"([^"]+)"', content)
        for status in statuses:
            print(f"  {status[0]} = {status[1]}")

def check_frontend_enums():
    """检查前端枚举值"""
    print("\n=== 前端枚举值检查 ===")
    
    frontend_path = Path("frontend/src/views/admin")
    
    # 检查用户管理
    user_mgmt_path = frontend_path / "UserManagement.vue"
    if user_mgmt_path.exists():
        print("用户管理页面选项:")
        content = user_mgmt_path.read_text(encoding='utf-8')
        options = re.findall(r'<el-option[^>]*label="([^"]+)"[^>]*value="([^"]+)"', content)
        for opt in options:
            print(f"  {opt[0]} = {opt[1]}")
    
    # 检查课程管理
    course_mgmt_path = frontend_path / "CourseManagement.vue"
    if course_mgmt_path.exists():
        print("\n课程管理页面选项:")
        content = course_mgmt_path.read_text(encoding='utf-8')
        options = re.findall(r'<el-option[^>]*label="([^"]+)"[^>]*value="([^"]+)"', content)
        for opt in options:
            if opt[1] not in ['', 'all']:  # 过滤空值
                print(f"  {opt[0]} = {opt[1]}")
    
    # 检查产品管理
    product_mgmt_path = frontend_path / "ProductManagement.vue"
    if product_mgmt_path.exists():
        print("\n产品管理页面选项:")
        content = product_mgmt_path.read_text(encoding='utf-8')
        options = re.findall(r'<el-option[^>]*label="([^"]+)"[^>]*value="([^"]+)"', content)
        radios = re.findall(r'<el-radio[^>]*label="([^"]+)">([^<]+)</el-radio>', content)
        
        for opt in options:
            if opt[1] not in ['', 'all']:
                print(f"  {opt[0]} = {opt[1]}")
        for radio in radios:
            print(f"  {radio[1]} = {radio[0]}")

def main():
    print("前后端字段一致性检查")
    print("=" * 50)
    
    # 切换到项目根目录
    os.chdir(Path(__file__).parent.parent)
    
    try:
        check_backend_enums()
        check_frontend_enums()
        
        print("\n=== 检查完成 ===")
        print("请人工对比上述输出，查找不匹配的字段值")
        
    except Exception as e:
        print(f"检查过程中出现错误: {e}")

if __name__ == "__main__":
    main()