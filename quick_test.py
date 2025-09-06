#!/usr/bin/env python3
"""
快速测试脚本 - 检查平台是否正常运行
"""
import sys
import requests
import time
import subprocess
import os
from pathlib import Path

def print_status(message, status="info"):
    colors = {
        "info": "\033[94m",     # 蓝色
        "success": "\033[92m",  # 绿色
        "warning": "\033[93m",  # 黄色
        "error": "\033[91m",    # 红色
        "reset": "\033[0m"      # 重置
    }
    
    prefix = {
        "info": "ℹ️",
        "success": "✅", 
        "warning": "⚠️",
        "error": "❌"
    }
    
    print(f"{colors[status]}{prefix[status]} {message}{colors['reset']}")

def check_service(url, name, timeout=5):
    """检查服务是否可用"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print_status(f"{name} 运行正常", "success")
            return True
        else:
            print_status(f"{name} 返回状态码: {response.status_code}", "warning")
            return False
    except requests.exceptions.ConnectionError:
        print_status(f"{name} 连接失败 - 服务可能未启动", "error")
        return False
    except requests.exceptions.Timeout:
        print_status(f"{name} 请求超时", "error")
        return False
    except Exception as e:
        print_status(f"{name} 检查失败: {str(e)}", "error")
        return False

def test_api_endpoints():
    """测试主要API端点"""
    endpoints = [
        ("http://localhost:8000/api/health", "健康检查"),
        ("http://localhost:8000/api/", "API根路径"),
        ("http://localhost:8000/docs", "API文档"),
        ("http://localhost:8000/api/courses/", "课程列表"),
        ("http://localhost:8000/api/products/", "产品列表"),
        ("http://localhost:8000/api/experts/", "专家列表"),
    ]
    
    print_status("测试API端点...", "info")
    success_count = 0
    
    for url, name in endpoints:
        if check_service(url, name):
            success_count += 1
        time.sleep(0.5)  # 避免请求过快
    
    return success_count, len(endpoints)

def check_database():
    """检查数据库"""
    db_file = Path("backend/tcm_backend.db")
    if db_file.exists():
        print_status("数据库文件存在", "success")
        return True
    else:
        print_status("数据库文件不存在", "error")
        return False

def check_processes():
    """检查进程是否运行"""
    backend_pid = Path("backend.pid")
    frontend_pid = Path("frontend.pid")
    
    processes_running = 0
    
    if backend_pid.exists():
        try:
            with open(backend_pid, 'r') as f:
                pid = int(f.read().strip())
            # 检查进程是否存在（简单方法）
            os.kill(pid, 0)
            print_status("后端进程运行中", "success")
            processes_running += 1
        except (OSError, ProcessLookupError, ValueError):
            print_status("后端进程未运行", "error")
    else:
        print_status("未找到后端进程文件", "warning")
    
    if frontend_pid.exists():
        try:
            with open(frontend_pid, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            print_status("前端进程运行中", "success") 
            processes_running += 1
        except (OSError, ProcessLookupError, ValueError):
            print_status("前端进程未运行", "error")
    else:
        print_status("未找到前端进程文件", "warning")
    
    return processes_running

def generate_test_report():
    """生成测试报告"""
    print("\n" + "="*50)
    print_status("中医健康平台 - 快速测试报告", "info")
    print("="*50)
    
    # 检查进程
    print("\n🔄 检查服务进程:")
    running_processes = check_processes()
    
    # 检查数据库
    print("\n💾 检查数据库:")
    db_ok = check_database()
    
    # 测试前端
    print("\n🌐 检查前端服务:")
    frontend_ok = check_service("http://localhost:5173", "前端页面", 3)
    
    # 测试后端API
    print("\n🔧 检查后端API:")
    backend_ok = check_service("http://localhost:8000", "后端服务", 3)
    
    # 测试具体API端点
    if backend_ok:
        print("\n📡 测试API端点:")
        success_apis, total_apis = test_api_endpoints()
    else:
        success_apis, total_apis = 0, 0
    
    # 生成总结
    print("\n" + "="*50)
    print_status("测试总结", "info")
    print("="*50)
    
    total_score = 0
    max_score = 4
    
    if running_processes >= 1:
        total_score += 1
    if db_ok:
        total_score += 1  
    if frontend_ok:
        total_score += 1
    if backend_ok:
        total_score += 1
    
    print(f"📊 总体状态: {total_score}/{max_score} 项检查通过")
    print(f"🔧 API端点: {success_apis}/{total_apis} 个正常")
    
    if total_score == max_score and success_apis >= total_apis * 0.8:
        print_status("🎉 平台运行完美！可以开始使用了", "success")
        print("\n📱 访问地址:")
        print("   前端: http://localhost:5173")
        print("   管理后台: http://localhost:5173/admin") 
        print("   API文档: http://localhost:8000/docs")
        print("\n👤 测试账户:")
        print("   管理员: admin@tcm.com / admin123")
        print("   用户: user@tcm.com / user123")
        
    elif total_score >= max_score * 0.5:
        print_status("⚠️ 平台部分功能正常，可能需要检查", "warning")
        print("\n🔧 建议:")
        if not backend_ok:
            print("   - 检查后端是否启动: ./start.sh")
        if not frontend_ok:
            print("   - 检查前端是否启动: cd frontend && npm run dev")
        if not db_ok:
            print("   - 重新初始化数据库: ./setup.sh")
            
    else:
        print_status("❌ 平台存在严重问题，需要重新设置", "error")
        print("\n🆘 解决方案:")
        print("   1. 停止所有服务: ./stop.sh")
        print("   2. 重新初始化: ./setup.sh")
        print("   3. 检查日志: tail -f logs/*.log")

if __name__ == "__main__":
    try:
        generate_test_report()
    except KeyboardInterrupt:
        print_status("\n测试被用户中断", "warning")
        sys.exit(0)
    except Exception as e:
        print_status(f"测试过程中发生错误: {e}", "error")
        sys.exit(1)