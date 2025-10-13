#!/usr/bin/env python3
"""
更新商品显示数据的脚本
"""
import requests
import json

# API配置
API_BASE = "http://localhost:8001"
LOGIN_URL = f"{API_BASE}/api/auth/simple-login"
PRODUCT_URL = f"{API_BASE}/api/products-simple/1"

def main():
    # 1. 先登录获取token
    login_data = {
        "username": "admin@tcm.com",
        "password": "admin123"
    }

    print("正在登录...")
    login_response = requests.post(LOGIN_URL, json=login_data)

    if not login_response.ok:
        print(f"登录失败: {login_response.status_code}")
        print(login_response.text)
        return

    login_result = login_response.json()
    if not login_result.get('success'):
        print(f"登录失败: {login_result.get('message')}")
        return

    token = login_result['data']['token']
    print("登录成功!")

    # 2. 更新商品信息
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    product_data = {
        "name": "优质人参",
        "description": "精选长白山野生人参，具有补气养血、提神醒脑的功效。适合体虚乏力、气血不足的人群使用。每日一次，温水送服。",
        "category": "HERBS",
        "price": "168.80",
        "stock_quantity": 50,
        "is_featured": True
    }

    print("正在更新商品信息...")
    response = requests.put(PRODUCT_URL, json=product_data, headers=headers)

    if response.ok:
        result = response.json()
        print("商品更新成功!")
        print(f"商品名称: {result.get('name', 'N/A')}")
        print(f"商品价格: ¥{result.get('price', 'N/A')}")
        print(f"库存数量: {result.get('stock_quantity', 'N/A')}")
        print(f"是否推荐: {result.get('is_featured', False)}")
    else:
        print(f"更新失败: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()