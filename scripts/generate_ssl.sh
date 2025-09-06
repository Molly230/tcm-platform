#!/bin/bash
# 生成自签名SSL证书（仅用于开发环境）

# 创建SSL目录
mkdir -p ssl

# 生成私钥
openssl genrsa -out ssl/key.pem 2048

# 生成证书签名请求
openssl req -new -key ssl/key.pem -out ssl/cert.csr -subj "/C=CN/ST=Beijing/L=Beijing/O=TCM Platform/OU=IT/CN=localhost"

# 生成自签名证书
openssl x509 -req -days 365 -in ssl/cert.csr -signkey ssl/key.pem -out ssl/cert.pem

# 清理临时文件
rm ssl/cert.csr

echo "SSL证书已生成在 ssl/ 目录"
echo "注意：这是自签名证书，仅用于开发环境"
echo "生产环境请使用Let's Encrypt或购买正式证书"