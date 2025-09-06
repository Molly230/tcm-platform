#!/usr/bin/env python3
"""
管理后台API测试脚本
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

class AdminAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        
    def login(self, email="admin@tcm.com", password="admin123"):
        """管理员登录"""
        print("🔐 正在登录管理员账户...")
        
        try:
            response = self.session.post(
                f"{BASE_URL}/api/auth/login",
                data={
                    "username": email,
                    "password": password
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })
                print(f"✅ 登录成功! 用户: {data.get('user', {}).get('email', email)}")
                return True
            else:
                print(f"❌ 登录失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 登录异常: {e}")
            return False
    
    def test_statistics(self):
        """测试统计数据API"""
        print("\n📊 测试统计数据API...")
        
        try:
            response = self.session.get(f"{BASE_URL}/api/admin/statistics")
            
            if response.status_code == 200:
                stats = response.json()
                print("✅ 统计数据获取成功!")
                
                # 显示关键统计
                overview = stats.get("overview", {})
                print(f"   总用户数: {overview.get('total_users', 0)}")
                print(f"   总专家数: {overview.get('total_experts', 0)}")
                print(f"   总商品数: {overview.get('total_products', 0)}")
                print(f"   总订单数: {overview.get('total_orders', 0)}")
                print(f"   总收入: ¥{overview.get('total_revenue', 0)}")
                return True
            else:
                print(f"❌ 统计数据获取失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 统计数据异常: {e}")
            return False
    
    def test_experts(self):
        """测试专家管理API"""
        print("\n👨‍⚕️ 测试专家管理API...")
        
        try:
            # 获取专家列表
            response = self.session.get(f"{BASE_URL}/api/admin/experts")
            
            if response.status_code == 200:
                experts = response.json()
                print(f"✅ 专家列表获取成功! 共 {len(experts)} 位专家")
                
                if experts:
                    expert = experts[0]
                    print(f"   专家: {expert.get('name')} ({expert.get('title')})")
                    
                    # 测试获取专家评价
                    expert_id = expert.get('id')
                    if expert_id:
                        reviews_response = self.session.get(f"{BASE_URL}/api/admin/experts/{expert_id}/reviews")
                        if reviews_response.status_code == 200:
                            reviews = reviews_response.json()
                            print(f"   专家评价数: {len(reviews)}")
                
                return True
            else:
                print(f"❌ 专家列表获取失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 专家管理异常: {e}")
            return False
    
    def test_products(self):
        """测试商品管理API"""
        print("\n🛒 测试商品管理API...")
        
        try:
            response = self.session.get(f"{BASE_URL}/api/admin/products")
            
            if response.status_code == 200:
                products = response.json()
                print(f"✅ 商品列表获取成功! 共 {len(products)} 个商品")
                
                if products:
                    product = products[0]
                    print(f"   商品: {product.get('name')} (¥{product.get('price', 0)})")
                
                return True
            else:
                print(f"❌ 商品列表获取失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 商品管理异常: {e}")
            return False
    
    def test_orders(self):
        """测试订单管理API"""
        print("\n📦 测试订单管理API...")
        
        try:
            response = self.session.get(f"{BASE_URL}/api/admin/orders")
            
            if response.status_code == 200:
                orders = response.json()
                print(f"✅ 订单列表获取成功! 共 {len(orders)} 个订单")
                
                if orders:
                    order = orders[0]
                    print(f"   订单: {order.get('order_number')} (¥{order.get('total_amount', 0)})")
                
                return True
            else:
                print(f"❌ 订单列表获取失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 订单管理异常: {e}")
            return False
    
    def test_consultations(self):
        """测试咨询管理API"""
        print("\n💬 测试咨询管理API...")
        
        try:
            response = self.session.get(f"{BASE_URL}/api/admin/consultations")
            
            if response.status_code == 200:
                consultations = response.json()
                print(f"✅ 咨询列表获取成功! 共 {len(consultations)} 个咨询")
                
                if consultations:
                    consultation = consultations[0]
                    print(f"   咨询: {consultation.get('title', 'N/A')} ({consultation.get('type', 'N/A')})")
                
                return True
            else:
                print(f"❌ 咨询列表获取失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 咨询管理异常: {e}")
            return False
    
    def test_users(self):
        """测试用户管理API"""
        print("\n👥 测试用户管理API...")
        
        try:
            response = self.session.get(f"{BASE_URL}/api/admin/users")
            
            if response.status_code == 200:
                users = response.json()
                print(f"✅ 用户列表获取成功! 共 {len(users)} 个用户")
                
                if users:
                    user = users[0]
                    print(f"   用户: {user.get('username')} ({user.get('email')})")
                
                return True
            else:
                print(f"❌ 用户列表获取失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 用户管理异常: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始管理后台API测试...\n")
        
        # 登录
        if not self.login():
            print("❌ 无法登录，测试终止!")
            return
        
        # 运行各项测试
        tests = [
            self.test_statistics,
            self.test_experts,
            self.test_products,
            self.test_orders,
            self.test_consultations,
            self.test_users
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except:
                failed += 1
        
        print(f"\n📋 测试结果: ✅ {passed} 通过, ❌ {failed} 失败")
        
        if failed == 0:
            print("🎉 所有管理后台API测试通过!")
        else:
            print("⚠️ 部分测试失败，请检查相关接口")

def main():
    """主函数"""
    tester = AdminAPITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()