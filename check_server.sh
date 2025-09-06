#!/bin/bash
# 服务器健康检查脚本

SERVER_IP="47.97.0.35"
DOMAIN="www.tcmlife.top"

echo "🔍 中医健康平台服务器检查"
echo "================================"

# 1. 网络连通性检查
echo "1. 检查服务器网络连通性..."
if ping -c 3 $SERVER_IP > /dev/null 2>&1; then
    echo "✅ 服务器IP $SERVER_IP 可以访问"
else
    echo "❌ 服务器IP $SERVER_IP 无法访问"
    echo "   请检查："
    echo "   - 阿里云控制台服务器状态"
    echo "   - 安全组配置"
    echo "   - 服务器是否已关机"
    exit 1
fi

# 2. 域名解析检查
echo "2. 检查域名解析..."
RESOLVED_IP=$(nslookup $DOMAIN | grep "Address:" | tail -1 | awk '{print $2}')
if [ "$RESOLVED_IP" = "$SERVER_IP" ]; then
    echo "✅ 域名 $DOMAIN 解析正确 -> $SERVER_IP"
else
    echo "⚠️  域名解析异常: $DOMAIN -> $RESOLVED_IP (期望: $SERVER_IP)"
fi

# 3. SSH连接检查
echo "3. 检查SSH连接..."
if timeout 10 ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no root@$SERVER_IP "echo 'SSH连接正常'" 2>/dev/null; then
    echo "✅ SSH连接正常"
    
    # 4. 服务器基本状态检查
    echo "4. 检查服务器状态..."
    ssh root@$SERVER_IP << 'REMOTE_COMMANDS'
        echo "   CPU使用率: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')"
        echo "   内存使用: $(free -h | awk 'NR==2{printf "%.1f%%", $3*100/$2 }')"
        echo "   磁盘使用: $(df -h / | awk 'NR==2{print $5}')"
        
        # Docker状态检查
        if command -v docker &> /dev/null; then
            echo "   Docker: 已安装"
            if systemctl is-active --quiet docker; then
                echo "   Docker服务: 运行中"
            else
                echo "   Docker服务: 未运行"
            fi
        else
            echo "   Docker: 未安装"
        fi
        
        # 检查项目目录
        if [ -d "/var/www/tcm-platform" ]; then
            echo "   项目目录: 存在"
            cd /var/www/tcm-platform
            echo "   Git分支: $(git branch --show-current 2>/dev/null || echo '未知')"
            echo "   最新提交: $(git log -1 --oneline 2>/dev/null || echo '无法获取')"
        else
            echo "   项目目录: 不存在"
        fi
REMOTE_COMMANDS
    
else
    echo "❌ SSH连接失败"
    echo "   可能原因："
    echo "   - SSH服务未启动"
    echo "   - 防火墙阻止22端口"
    echo "   - 服务器已关机"
    exit 1
fi

# 5. Web服务检查
echo "5. 检查Web服务..."
if curl -I --connect-timeout 10 http://$DOMAIN > /dev/null 2>&1; then
    echo "✅ Web服务响应正常"
else
    echo "❌ Web服务无响应"
fi

echo ""
echo "🎯 检查完成！"
echo "如果所有检查都通过，可以执行部署："
echo "   ./deploy_git.sh"