# 🚀 中医健康平台部署检查清单

## 阶段1: 服务器基础检查 ✅
**必须完成后才能进入下一阶段**

### 1.1 服务器连通性检查
```bash
# 本地检查服务器是否在线
ping -n 4 47.97.0.35
nslookup www.tcmlife.top

# SSH连接测试
ssh root@47.97.0.35
```

### 1.2 服务器状态检查
```bash
# 在服务器上执行
systemctl status docker
systemctl status nginx
df -h  # 检查磁盘空间
free -m  # 检查内存
```

### 1.3 网络环境检查
```bash
# 测试Docker Hub连接
curl -I https://registry-1.docker.io/v2/
# 测试GitHub连接  
curl -I https://github.com
```

---

## 阶段2: 部署脚本修复 🔧
**修复已知问题**

### 2.1 修复deploy_git.sh占位符
```bash
# 当前问题行36: 
# git clone https://github.com/yourusername/tcm-platform.git
# 应该改为:
git clone https://github.com/Molly230/tcm-platform.git
```

### 2.2 创建生产环境配置
```bash
# 在服务器上创建 /var/www/tcm-platform/.env
DATABASE_URL=postgresql://tcm_user:password@db:5432/tcm_db
REDIS_URL=redis://redis:6379
SECRET_KEY=your-production-secret-key
DOMAIN=tcmlife.top
```

---

## 阶段3: 分步部署验证 🎯

### 3.1 基础环境部署
```bash
# 只启动基础服务
docker-compose up -d db redis nginx
docker-compose ps  # 确认服务状态
```

### 3.2 后端服务部署
```bash
# 启动后端
docker-compose up -d backend
# 检查日志
docker-compose logs backend
# 测试API
curl http://localhost:8000/health
```

### 3.3 前端服务部署
```bash
# 启动前端
docker-compose up -d frontend
# 测试页面
curl -I http://localhost
```

### 3.4 数据库初始化
```bash
# 执行数据库迁移
docker-compose exec backend alembic upgrade head
# 创建管理员
docker-compose exec backend python create_admin.py
# 初始化数据
docker-compose exec backend python seed_data.py
```

---

## 阶段4: 功能验证 ✨

### 4.1 关键页面检查
- [ ] 首页正常加载: http://www.tcmlife.top/
- [ ] 课程页面: http://www.tcmlife.top/courses
- [ ] 登录页面: http://www.tcmlife.top/login
- [ ] 注册页面: http://www.tcmlife.top/register

### 4.2 API功能检查
```bash
# 测试用户注册
curl -X POST http://www.tcmlife.top/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","username":"testuser"}'

# 测试课程API
curl http://www.tcmlife.top/api/courses
```

### 4.3 核心流程检查
- [ ] 用户注册流程
- [ ] 用户登录流程  
- [ ] 课程浏览流程
- [ ] 课程购买流程

---

## 阶段5: 性能和安全 🔒

### 5.1 SSL证书配置
```bash
# 安装Let's Encrypt证书
certbot --nginx -d tcmlife.top -d www.tcmlife.top
```

### 5.2 防火墙配置
```bash
# 开放必要端口
ufw allow 80
ufw allow 443
ufw allow 22
ufw enable
```

### 5.3 监控配置
```bash
# 设置日志轮转
docker-compose exec backend python -c "import logging; logging.info('Test log')"
```

---

## 🆘 故障排除指南

### 问题1: 服务器无法连接
**症状**: ping超时，SSH连接失败
**解决**: 
1. 检查阿里云控制台服务器状态
2. 检查安全组规则
3. 重启服务器实例

### 问题2: Docker拉取镜像失败
**症状**: registry-1.docker.io连接超时
**解决**:
1. 配置Docker镜像加速器
2. 使用阿里云镜像仓库
3. 手动构建镜像

### 问题3: 数据库连接失败  
**症状**: Connection refused
**解决**:
1. 检查PostgreSQL容器状态
2. 检查环境变量配置
3. 检查网络配置

### 问题4: 前端页面404
**症状**: nginx返回404
**解决**:
1. 检查nginx配置文件
2. 检查前端构建产物
3. 检查域名解析

---

## 📋 最终检查清单

部署完成后，必须全部通过：

- [ ] 所有Docker容器运行正常
- [ ] 网站https://www.tcmlife.top正常访问
- [ ] 用户可以正常注册登录
- [ ] 课程页面数据正常显示
- [ ] 支付流程可以正常发起
- [ ] 管理后台可以正常访问
- [ ] SSL证书有效
- [ ] 日志记录正常

**只有全部通过，才算部署成功！**