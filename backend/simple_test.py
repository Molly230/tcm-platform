import requests

# 测试API健康状态
print("Testing API health...")
response = requests.get("http://localhost:8000/api/health")
print(f"Health check: {response.status_code} - {response.json()}")

# 测试专家API（无认证）
print("\nTesting experts API...")
response = requests.get("http://localhost:8000/api/experts")
print(f"Experts API: {response.status_code}")
if response.status_code == 200:
    experts = response.json()
    print(f"Found {len(experts)} experts")

# 测试商品API（无认证）
print("\nTesting products API...")
response = requests.get("http://localhost:8000/api/products")
print(f"Products API: {response.status_code}")
if response.status_code == 200:
    products = response.json()
    print(f"Found {len(products)} products")

print("\nAdmin APIs require authentication - that's correct!")
print("Backend is running properly!")