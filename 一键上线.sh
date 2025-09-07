#!/bin/bash

echo "================================================"
echo "🚀 一键上线脚本 - 人话版"
echo "================================================"
echo "这个脚本会自动帮你安装和配置所有东西"
echo "你只需要等着就行，大概需要5-10分钟"
echo "================================================"

# 获取服务器IP
SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || echo "未知")
echo "📍 你的服务器IP: $SERVER_IP"
echo ""

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请用管理员身份运行："
    echo "sudo ./一键上线.sh"
    exit 1
fi

echo "🔧 第1步：安装基础软件..."
apt update >/dev/null 2>&1
apt install -y python3 python3-pip nodejs npm nginx curl >/dev/null 2>&1
echo "✅ 基础软件安装完成"

echo ""
echo "📁 第2步：准备项目文件..."
cd /var/www
if [ ! -d "tcm-platform" ]; then
    echo "⚠️  未发现项目文件，请手动上传项目到 /var/www/tcm-platform"
    echo "或者如果你的代码在GitHub，请运行："
    echo "git clone https://github.com/你的用户名/项目名.git tcm-platform"
    exit 1
fi

cd tcm-platform
echo "✅ 项目文件检查完成"

echo ""
echo "🐍 第3步：安装Python依赖..."
if [ -f "backend/requirements.txt" ]; then
    cd backend
    pip3 install -r requirements.txt >/dev/null 2>&1
    cd ..
    echo "✅ Python依赖安装完成"
else
    echo "⚠️  未找到requirements.txt，跳过Python依赖"
fi

echo ""
echo "🌐 第4步：构建前端..."
if [ -f "frontend/package.json" ]; then
    cd frontend
    npm install >/dev/null 2>&1
    npm run build >/dev/null 2>&1
    cp -r dist/* /var/www/html/ 2>/dev/null
    cd ..
    echo "✅ 前端构建完成"
else
    echo "⚠️  未找到前端项目，跳过前端构建"
fi

echo ""
echo "🔧 第5步：配置网页服务器..."
cat > /etc/nginx/sites-available/default << 'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /var/www/html;
    index index.html index.htm;
    server_name _;
    
    # 前端页面
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # 静态文件
    location /uploads {
        alias /var/www/tcm-platform/backend/uploads;
    }
}
EOF

nginx -t >/dev/null 2>&1
systemctl restart nginx
echo "✅ 网页服务器配置完成"

echo ""
echo "🚀 第6步：启动后端服务..."
cd /var/www/tcm-platform/backend

# 创建启动脚本
cat > start.sh << 'EOF'
#!/bin/bash
export DATABASE_URL="sqlite:///./tcm_backend.db"
export DEBUG=False
export SERVER_HOST="http://0.0.0.0:8000"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
EOF

chmod +x start.sh

# 后台启动
nohup ./start.sh > /var/log/backend.log 2>&1 &
echo "✅ 后端服务启动完成"

echo ""
echo "⏳ 等待服务完全启动..."
sleep 10

# 检查服务是否正常
if curl -s http://localhost >/dev/null && curl -s http://localhost:8000 >/dev/null; then
    echo ""
    echo "================================================"
    echo "🎉 恭喜！你的网站已经成功上线了！"
    echo "================================================"
    echo ""
    echo "🌐 访问你的网站："
    echo "   http://$SERVER_IP"
    echo ""
    echo "🔑 默认管理员账号："
    echo "   邮箱: admin@tcm.com"
    echo "   密码: admin123"
    echo ""
    echo "📊 检查网站状态："
    echo "   网页服务器: systemctl status nginx"
    echo "   后端服务: ps aux | grep uvicorn"
    echo "   后端日志: tail -f /var/log/backend.log"
    echo ""
    echo "🔄 重启服务命令："
    echo "   重启网页: systemctl restart nginx"
    echo "   重启后端: pkill -f uvicorn && cd /var/www/tcm-platform/backend && nohup ./start.sh > /var/log/backend.log 2>&1 &"
    echo ""
    echo "================================================"
    echo "🎊 你现在拥有了一个专业的网站！"
    echo "================================================"
else
    echo ""
    echo "⚠️  网站可能没有完全启动成功"
    echo "请检查："
    echo "1. 网页服务器: systemctl status nginx"
    echo "2. 后端服务: ps aux | grep uvicorn" 
    echo "3. 后端日志: tail -f /var/log/backend.log"
    echo ""
    echo "如果有问题，可以重新运行这个脚本"
fi

echo ""
echo "💡 小贴士："
echo "• 以后更新网站：git pull && 重新运行这个脚本"
echo "• 有问题就重新运行这个脚本"
echo "• 记住你的服务器IP: $SERVER_IP"