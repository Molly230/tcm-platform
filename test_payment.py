#!/usr/bin/env python3
"""
支付系统测试脚本
"""
import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"

def test_payment_flow():
    """测试完整的支付流程"""
    print("开始测试支付系统...")
    
    # 1. 测试支付创建
    print("\n1. 测试支付创建...")
    test_order_id = f"ORDER_TEST_{int(time.time())}"
    
    try:
        response = requests.post(f"{BASE_URL}/api/reliable-pay/create", json={
            "order_id": test_order_id,
            "payment_method": "alipay_qr"
        })
        
        if response.status_code == 200:
            result = response.json()
            print("支付创建成功")
            print(f"   订单号: {test_order_id}")
            print(f"   支付URL: {result.get('payment_url', '')[:50]}...")
            print(f"   Charge ID: {result.get('charge_id', '')}")
            charge_id = result.get('charge_id', '')
        else:
            print(f"❌ 支付创建失败: {response.status_code}")
            print(f"   错误详情: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 支付创建异常: {e}")
        return False
    
    # 2. 测试状态查询
    print("\n2. 测试支付状态查询...")
    try:
        response = requests.get(f"{BASE_URL}/api/reliable-pay/status/{test_order_id}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 状态查询成功")
            print(f"   订单状态: {result.get('order_status', 'unknown')}")
            print(f"   支付状态: {result.get('payment_status', 'unknown')}")
            print(f"   模拟模式: {result.get('mock_mode', False)}")
        else:
            print(f"⚠️  状态查询失败: {response.status_code}")
            print(f"   错误详情: {response.text}")
            
    except Exception as e:
        print(f"❌ 状态查询异常: {e}")
    
    # 3. 测试模拟支付成功
    print("\n3. 测试模拟支付成功...")
    try:
        response = requests.post(f"{BASE_URL}/api/reliable-pay/simulate-success/{test_order_id}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 模拟支付成功")
            print(f"   消息: {result.get('message', '')}")
        else:
            print(f"❌ 模拟支付失败: {response.status_code}")
            print(f"   错误详情: {response.text}")
            
    except Exception as e:
        print(f"❌ 模拟支付异常: {e}")
    
    # 4. 再次查询状态确认
    print("\n4. 确认支付状态更新...")
    try:
        response = requests.get(f"{BASE_URL}/api/reliable-pay/status/{test_order_id}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 最终状态确认")
            print(f"   订单状态: {result.get('order_status', 'unknown')}")
            print(f"   支付状态: {result.get('payment_status', 'unknown')}")
            if result.get('paid_at'):
                print(f"   支付时间: {result.get('paid_at', '')}")
        else:
            print(f"❌ 最终状态查询失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 最终状态查询异常: {e}")
    
    return True

def test_different_payment_methods():
    """测试不同支付方式"""
    print("\n🎯 测试不同支付方式...")
    
    methods = ["alipay_qr", "alipay", "wechat"]
    
    for method in methods:
        print(f"\n测试 {method}:")
        test_order_id = f"ORDER_{method.upper()}_{int(time.time())}"
        
        try:
            response = requests.post(f"{BASE_URL}/api/reliable-pay/create", json={
                "order_id": test_order_id,
                "payment_method": method
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {method} 支付创建成功")
                print(f"   支付URL: {result.get('payment_url', '')[:60]}...")
            else:
                print(f"❌ {method} 支付创建失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {method} 测试异常: {e}")

def test_api_health():
    """测试API健康状态"""
    print("\n🏥 测试API健康状态...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ API服务正常")
        else:
            print(f"⚠️  API服务异常: {response.status_code}")
    except Exception as e:
        print(f"❌ API服务连接失败: {e}")
        print("   请确保后端服务已启动: uvicorn app.main:app --reload")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 中医健康平台 - 支付系统测试")
    print("=" * 60)
    
    # 先测试API连通性
    if not test_api_health():
        sys.exit(1)
    
    # 测试完整支付流程
    test_payment_flow()
    
    # 测试不同支付方式
    test_different_payment_methods()
    
    print("\n" + "=" * 60)
    print("🎉 测试完成！")
    print("\n💡 使用说明:")
    print("1. 启动后端: cd backend && uvicorn app.main:app --reload")
    print("2. 启动前端: cd frontend && npm run dev")
    print("3. 访问支付页面: http://localhost:5173/payment/ORDER_123")
    print("=" * 60)