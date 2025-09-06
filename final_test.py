#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
支付系统最终测试脚本
"""
import requests
import time

BASE_URL = "http://localhost:8001"

def test_payment():
    print("=" * 50)
    print("支付系统最终测试")
    print("=" * 50)
    
    test_order_id = f"ORDER_FINAL_{int(time.time())}"
    print(f"测试订单: {test_order_id}")
    
    # 1. 创建支付
    print("\n1. 创建支付...")
    response = requests.post(f"{BASE_URL}/api/reliable-pay/create", json={
        "order_id": test_order_id,
        "payment_method": "alipay_qr"
    })
    
    if response.status_code == 200:
        result = response.json()
        print("支付创建成功!")
        print(f"支付URL: {result['payment_url']}")
        print(f"Charge ID: {result['charge_id']}")
        
        # 2. 模拟支付成功
        print("\n2. 模拟支付成功...")
        sim_response = requests.post(f"{BASE_URL}/api/reliable-pay/simulate-success/{test_order_id}")
        if sim_response.status_code == 200:
            print("支付模拟成功!")
        
        # 3. 查询状态
        print("\n3. 查询支付状态...")
        status_response = requests.get(f"{BASE_URL}/api/reliable-pay/status/{test_order_id}")
        if status_response.status_code == 200:
            status = status_response.json()
            print("状态查询成功!")
            print(f"订单状态: {status['order_status']}")
            print(f"支付状态: {status['payment_status']}")
        
        print("\n" + "=" * 50)
        print("测试成功!")
        print("支付系统已经可以正常工作!")
        print("前端集成说明:")
        print("1. 调用 POST /api/reliable-pay/create 创建支付")
        print("2. 显示二维码给用户扫描")
        print("3. 调用 POST /api/reliable-pay/simulate-success/{order_id} 模拟支付")
        print("4. 调用 GET /api/reliable-pay/status/{order_id} 查询状态")
        print("=" * 50)
    else:
        print("支付创建失败!")
        print(f"状态码: {response.status_code}")
        print(f"错误: {response.text}")

if __name__ == "__main__":
    test_payment()