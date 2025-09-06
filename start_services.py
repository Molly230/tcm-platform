#!/usr/bin/env python3
"""
优化的服务启动脚本
避免重复启动服务，提供服务状态检查和管理功能
"""

import os
import sys
import subprocess
import time
import requests
import signal
from pathlib import Path

# 端口配置
BACKEND_PORT = 8000
FRONTEND_PORT = 3001

def check_port_in_use(port):
    """检查端口是否被占用"""
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('127.0.0.1', port))
            return result == 0
    except:
        return False

def check_service_health(url):
    """检查服务健康状态"""
    try:
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except:
        return False

def kill_process_on_port(port):
    """杀死占用指定端口的进程"""
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(
                f'netstat -ano | findstr :{port}', 
                shell=True, capture_output=True, text=True
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'LISTENING' in line:
                        pid = line.split()[-1]
                        subprocess.run(f'taskkill /F /PID {pid}', shell=True)
                        print(f"✅ 已关闭端口 {port} 上的进程 (PID: {pid})")
        else:  # Unix-like
            subprocess.run(f'lsof -ti:{port} | xargs kill -9', shell=True)
            print(f"✅ 已关闭端口 {port} 上的进程")
    except Exception as e:
        print(f"❌ 关闭端口 {port} 上的进程失败: {e}")

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    
    if check_port_in_use(BACKEND_PORT):
        print(f"⚠️  端口 {BACKEND_PORT} 已被占用，检查是否为有效的后端服务...")
        if check_service_health(f"http://localhost:{BACKEND_PORT}/health"):
            print("✅ 后端服务已在运行且健康")
            return True
        else:
            print(f"❌ 端口 {BACKEND_PORT} 被占用但服务不健康，强制关闭...")
            kill_process_on_port(BACKEND_PORT)
            time.sleep(2)
    
    # 检查是否在backend目录
    if not os.path.exists("backend"):
        print("❌ 未找到 backend 目录，请在项目根目录运行此脚本")
        return False
    
    # 启动后端
    try:
        os.chdir("backend")
        subprocess.Popen(
            ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", str(BACKEND_PORT)],
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        os.chdir("..")
        
        # 等待服务启动
        print("⏳ 等待后端服务启动...")
        for i in range(30):  # 等待最多30秒
            if check_service_health(f"http://localhost:{BACKEND_PORT}/health"):
                print("✅ 后端服务启动成功")
                return True
            time.sleep(1)
        
        print("❌ 后端服务启动超时")
        return False
        
    except Exception as e:
        print(f"❌ 启动后端服务失败: {e}")
        return False

def start_frontend():
    """启动前端服务"""
    print("🚀 启动前端服务...")
    
    if check_port_in_use(FRONTEND_PORT):
        print(f"⚠️  端口 {FRONTEND_PORT} 已被占用，强制关闭...")
        kill_process_on_port(FRONTEND_PORT)
        time.sleep(2)
    
    # 检查是否在frontend目录
    if not os.path.exists("frontend"):
        print("❌ 未找到 frontend 目录，请在项目根目录运行此脚本")
        return False
    
    # 启动前端
    try:
        os.chdir("frontend")
        env = os.environ.copy()
        env['VITE_PORT'] = str(FRONTEND_PORT)
        
        subprocess.Popen(
            ["npm", "run", "dev"],
            env=env,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        os.chdir("..")
        
        # 等待服务启动
        print("⏳ 等待前端服务启动...")
        time.sleep(5)  # 前端启动通常需要更长时间
        
        if check_port_in_use(FRONTEND_PORT):
            print("✅ 前端服务启动成功")
            return True
        else:
            print("❌ 前端服务启动失败")
            return False
            
    except Exception as e:
        print(f"❌ 启动前端服务失败: {e}")
        return False

def show_status():
    """显示服务状态"""
    print("\n" + "="*50)
    print("📊 服务状态检查")
    print("="*50)
    
    backend_port_used = check_port_in_use(BACKEND_PORT)
    backend_healthy = check_service_health(f"http://localhost:{BACKEND_PORT}/health") if backend_port_used else False
    
    frontend_port_used = check_port_in_use(FRONTEND_PORT)
    
    print(f"后端服务 (:{BACKEND_PORT}): {'✅ 运行中' if backend_healthy else '❌ 未运行' if not backend_port_used else '⚠️  端口占用但不健康'}")
    print(f"前端服务 (:{FRONTEND_PORT}): {'✅ 运行中' if frontend_port_used else '❌ 未运行'}")
    
    if backend_healthy and frontend_port_used:
        print(f"\n🎉 所有服务运行正常!")
        print(f"🌐 前端访问: http://localhost:{FRONTEND_PORT}")
        print(f"📡 后端API: http://localhost:{BACKEND_PORT}/docs")
    
    print("="*50)

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "status":
            show_status()
            return
        elif command == "stop":
            print("🛑 停止所有服务...")
            kill_process_on_port(BACKEND_PORT)
            kill_process_on_port(FRONTEND_PORT)
            print("✅ 所有服务已停止")
            return
        elif command == "restart":
            print("🔄 重启所有服务...")
            kill_process_on_port(BACKEND_PORT)
            kill_process_on_port(FRONTEND_PORT)
            time.sleep(3)
        elif command in ["help", "-h", "--help"]:
            print("""
使用方法:
  python start_services.py        # 启动服务
  python start_services.py status # 检查状态
  python start_services.py stop   # 停止服务
  python start_services.py restart # 重启服务
  python start_services.py help   # 显示帮助
            """)
            return
    
    print("🚀 中医健康平台服务启动器")
    print("="*50)
    
    # 启动服务
    backend_success = start_backend()
    frontend_success = start_frontend()
    
    # 显示结果
    time.sleep(2)
    show_status()
    
    if backend_success and frontend_success:
        print("\n✨ 启动完成! 按 Ctrl+C 可查看完整状态")
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            show_status()

if __name__ == "__main__":
    main()