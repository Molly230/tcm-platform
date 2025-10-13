"""
重启后端服务并测试微信支付
"""
import os
import sys
import subprocess
import time
import requests
import json

print("=" * 60)
print("重启后端并测试微信支付")
print("=" * 60)

# 1. 杀掉旧进程
print("\n[1/6] 停止旧的后端进程...")
try:
    subprocess.run("taskkill /F /PID 656 /T", shell=True, capture_output=True)
    subprocess.run("taskkill /F /PID 9300 /T", shell=True, capture_output=True)
    print("OK - 旧进程已停止")
except:
    pass

time.sleep(2)

# 2. 启动新的后端
print("\n[2/6] 启动新后端服务...")
backend_dir = r"F:\360MoveData\Users\administered\Desktop\999\backend"
os.chdir(backend_dir)

# 在后台启动uvicorn
cmd = "start /B python -m uvicorn app.main:app --host 127.0.0.1 --port 8001"
subprocess.Popen(cmd, shell=True)

print("OK - 后端启动中，等待15秒...")
time.sleep(15)

# 3. 检查后端是否启动
print("\n[3/6] 检查后端状态...")
try:
    health_response = requests.get("http://localhost:8001/api/health", timeout=5)
    if health_response.status_code == 200:
        print("OK - 后端服务正常")
    else:
        print(f"WARN - 健康检查返回: {health_response.status_code}")
except Exception as e:
    print(f"ERROR - 后端未启动: {e}")
    print("请手动启动后端: uvicorn app.main:app --reload --port 8001")
    sys.exit(1)

# 4. 测试微信支付配置接口
print("\n[4/6] 测试微信支付配置...")
try:
    config_response = requests.get("http://localhost:8001/api/wechat-pay/config", timeout=5)
    if config_response.status_code == 200:
        config = config_response.json()
        print("OK - 微信支付配置接口正常")
        print(json.dumps(config, indent=2, ensure_ascii=False))

        mock_mode = config.get("config", {}).get("mock_mode")
        if mock_mode:
            print("\n!!! WARNING - 还是模拟模式，配置未生效 !!!")
        else:
            print("\n>>> SUCCESS - 真实支付模式已启用 <<<")
    elif config_response.status_code == 404:
        print("ERROR - 微信支付API不存在，代码未加载")
        print("说明uvicorn没有使用--reload参数，或者启动失败")
    else:
        print(f"ERROR - 配置接口返回: {config_response.status_code}")
        print(config_response.text)
except Exception as e:
    print(f"ERROR - 配置接口调用失败: {e}")

# 5. 登录获取token
print("\n[5/6] 登录测试账号...")
try:
    login_response = requests.post(
        "http://localhost:8001/api/auth/login",
        json={"username": "user@tcm.com", "password": "user123"},
        timeout=5
    )
    if login_response.status_code == 200:
        token = login_response.json().get("access_token")
        if token:
            print(f"OK - 登录成功")
        else:
            print("WARN - 登录成功但未返回token")
            token = None
    else:
        print(f"ERROR - 登录失败: {login_response.status_code}")
        print(login_response.text)
        token = None
except Exception as e:
    print(f"ERROR - 登录接口调用失败: {e}")
    token = None

# 6. 总结
print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)

print("\n后续操作:")
print("1. 打开浏览器: http://localhost:8001/docs")
print("2. 找到 '微信支付' 分组")
print("3. 测试 Native 支付接口")
print("\n如需完整测试，运行: python test_wechat_simple.py")
