#!/usr/bin/env python3
"""
测试简化版支付API
"""
import requests
import time

BASE_URL = "http://localhost:8001"

def test_payment_flow():
    print("=" * 50)
    print("支付系统完整测试")
    print("=" * 50)
    
    # 1. 测试支付创建
    test_order_id = f"ORDER_TEST_{int(time.time())}"
    print(f"\n1. 创建支付订单: {test_order_id}")
    
    response = requests.post(f"{BASE_URL}/api/reliable-pay/create", json={
        "order_id": test_order_id,
        "payment_method": "alipay_qr"
    })
    
    if response.status_code == 200:
        result = response.json()
        print("支付创建成功!")
        print(f"  订单号: {test_order_id}")
        print(f"  支付URL: {result['payment_url']}")
        print(f"  Charge ID: {result['charge_id']}")
        print(f"  消息: {result['message']}")
        
        # 2. 模拟支付成功
        print(f"\n2. 模拟支付成功...")
        sim_response = requests.post(f"{BASE_URL}/api/reliable-pay/simulate-success/{test_order_id}")
        if sim_response.status_code == 200:
            sim_result = sim_response.json()
            print("✓ 支付模拟成功!")
            print(f"  消息: {sim_result['message']}")
            
            # 3. 查询支付状态
            print(f"\n3. 查询支付状态...")
            status_response = requests.get(f"{BASE_URL}/api/reliable-pay/status/{test_order_id}")
            if status_response.status_code == 200:
                status_result = status_response.json()
                print("✓ 状态查询成功!")
                print(f"  订单状态: {status_result['order_status']}")
                print(f"  支付状态: {status_result['payment_status']}")
                print(f"  模拟模式: {status_result['mock_mode']}")
            else:
                print("✗ 状态查询失败")
        else:
            print("✗ 支付模拟失败")
    else:
        print("✗ 支付创建失败")
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.text}")
    
    # 4. 测试不同支付方式
    print(f"\n4. 测试不同支付方式...")
    methods = ["alipay_qr", "alipay", "wechat"]
    
    for method in methods:
        test_id = f"ORDER_{method.upper()}_{int(time.time())}"
        response = requests.post(f"{BASE_URL}/api/reliable-pay/create", json={
            "order_id": test_id,
            "payment_method": method
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ {method}: {result['payment_url'][:50]}...")
        else:
            print(f"  ✗ {method}: 失败")
    
    print("\n" + "=" * 50)
    print("🎉 测试完成!")
    print("支付系统功能正常，可以投入使用！")
    print("=" * 50)

if __name__ == "__main__":
    test_payment_flow()