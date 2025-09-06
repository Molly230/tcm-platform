#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的支付系统测试脚本
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_payment():
    """测试支付功能"""
    print("测试支付系统...")
    
    # 测试订单号
    test_order_id = f"ORDER_TEST_{int(time.time())}"
    
    print(f"1. 创建支付订单: {test_order_id}")
    
    try:
        # 创建支付
        response = requests.post(f"{BASE_URL}/api/reliable-pay/create", json={
            "order_id": test_order_id,
            "payment_method": "alipay_qr"
        })
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("支付创建成功!")
            print(f"支付URL: {result.get('payment_url', '')}")
            print(f"Charge ID: {result.get('charge_id', '')}")
            
            # 模拟支付成功
            print(f"\n2. 模拟支付成功...")
            sim_response = requests.post(f"{BASE_URL}/api/reliable-pay/simulate-success/{test_order_id}")
            if sim_response.status_code == 200:
                print("模拟支付成功!")
                sim_result = sim_response.json()
                print(f"结果: {sim_result.get('message', '')}")
            else:
                print(f"模拟支付失败: {sim_response.status_code}")
                print(f"错误: {sim_response.text}")
            
            # 查询状态
            print(f"\n3. 查询支付状态...")
            status_response = requests.get(f"{BASE_URL}/api/reliable-pay/status/{test_order_id}")
            if status_response.status_code == 200:
                status_result = status_response.json()
                print("状态查询成功!")
                print(f"订单状态: {status_result.get('order_status', 'unknown')}")
                print(f"支付状态: {status_result.get('payment_status', 'unknown')}")
            else:
                print(f"状态查询失败: {status_response.status_code}")
        else:
            print("支付创建失败!")
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"测试异常: {e}")

def test_health():
    """测试API健康"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("API服务正常")
            return True
        else:
            print(f"API服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"无法连接到API服务: {e}")
        print("请确保后端服务已启动: uvicorn app.main:app --reload")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("支付系统测试")
    print("=" * 50)
    
    if test_health():
        test_payment()
    
    print("\n" + "=" * 50)
    print("测试完成!")
    print("如需访问API文档: http://localhost:8000/docs")
    print("=" * 50)