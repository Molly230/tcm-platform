# 🚀 线上更新操作手册

**上线后要改内容？没问题！按这个流程走，安全无忧。**

## ⚡ 快速更新（5分钟搞定）

### 1. 小改动（文案、样式、图片）

```bash
# 1. 本地修改并提交
git add .
git commit -m "更新：修改内容描述"
git push origin main

# 2. 服务器拉取更新（仅前端）
ssh user@your-server
cd /var/www/tcm-platform
git pull origin main
cd frontend && npm run build
sudo cp -r dist/* /var/www/html/

# 3. 重新加载nginx（零停机）
sudo nginx -s reload
```

**✅ 优点：** 秒级更新，用户无感知  
**📝 适用：** 前端文案、CSS样式、图片更换

---

### 2. 功能更新（API、业务逻辑）

```bash
# 1. 先在预发布环境测试
./deploy_staging.sh deploy

# 2. 测试无误后一键部署生产环境
sudo ./update_production.sh update
```

**⏱️ 用时：** 约2-5分钟  
**📝 适用：** 后端功能、数据库更改、重大更新

---

## 📋 不同场景的更新方案

### 场景A: 改个页面文字
```bash
# 最简单，直接改前端代码
vim frontend/src/views/HomePage.vue  # 修改文字
git add . && git commit -m "修改首页文字"
git push origin main

# 服务器更新前端
ssh user@server "cd /var/www/tcm-platform && git pull && cd frontend && npm run build && sudo cp -r dist/* /var/www/html/"
```

### 场景B: 修改API接口  
```bash
# 修改后端代码
vim backend/app/api/users.py
git add . && git commit -m "修改用户API"
git push origin main

# 使用热更新脚本
sudo ./update_production.sh update
```

### 场景C: 新增数据库表/字段
```bash
# 1. 修改模型
vim backend/app/models/user.py

# 2. 生成迁移文件
cd backend && alembic revision --autogenerate -m "新增字段"

# 3. 提交代码
git add . && git commit -m "数据库：新增用户字段"
git push origin main

# 4. 部署（会自动执行数据库迁移）
sudo ./update_production.sh update
```

### 场景D: 紧急修复bug
```bash
# 直接在main分支修复
git checkout main
vim 修复bug的文件
git add . && git commit -m "紧急修复：描述bug"
git push origin main

# 立即热更新
sudo ./update_production.sh update
```

---

## 🎛️ 常用命令速查

### 检查系统状态
```bash
# 健康检查
curl http://你的域名.com/health/detailed

# 查看服务状态  
sudo docker-compose ps

# 查看日志
sudo docker-compose logs -f backend
```

### 备份和回滚
```bash
# 创建备份
sudo ./update_production.sh backup

# 紧急回滚
sudo ./update_production.sh rollback

# 查看当前版本
git describe --tags
```

### 监控命令
```bash
# 实时访问日志
sudo tail -f /var/log/nginx/access.log

# 系统资源
htop

# 数据库状态
sudo docker-compose exec db psql -U tcm_user -d tcm_platform -c "SELECT version();"
```

---

## 🚨 故障应急处理

### 1. 网站打不开了
```bash
# 检查服务状态
sudo docker-compose ps

# 重启所有服务
sudo docker-compose restart

# 如果还不行，回滚
sudo ./update_production.sh rollback
```

### 2. 数据库连接失败
```bash
# 检查数据库状态
sudo docker-compose exec db pg_isready

# 重启数据库
sudo docker-compose restart db

# 检查数据库连接配置
cat .env | grep DATABASE_URL
```

### 3. 前端显示空白页
```bash
# 检查前端文件
ls -la /var/www/html/

# 重新构建前端
cd frontend && npm run build && sudo cp -r dist/* /var/www/html/

# 检查nginx配置
sudo nginx -t && sudo nginx -s reload
```

---

## 📞 需要帮助时

### 自助检查清单
1. ✅ 健康检查是否通过？
2. ✅ 错误日志有没有异常？
3. ✅ 系统资源是否充足？
4. ✅ 第三方服务是否正常？

### 实用调试命令
```bash
# 一键健康检查
curl -s http://localhost:8000/health/detailed | python -m json.tool

# 查看最近的错误日志
sudo docker-compose logs --tail=50 backend | grep -i error

# 检查系统资源
df -h && free -m

# 测试数据库连接
sudo docker-compose exec backend python -c "from app.database import engine; print('DB OK' if engine.connect() else 'DB Failed')"
```

---

## ⭐ 最佳实践

### 1. 更新前
- 🔍 **先在预发布环境测试**
- 💾 **创建备份**
- ⏰ **选择用户较少的时间**
- 📢 **重要更新提前通知用户**

### 2. 更新中  
- 👀 **实时监控系统状态**
- 📊 **观察错误日志**
- ⚡ **准备好回滚方案**

### 3. 更新后
- ✅ **全面功能测试**
- 📈 **监控系统性能**
- 🗣️ **收集用户反馈**

---

## 🎯 记住这几个关键命令

```bash
# 简单更新（前端）
git pull && cd frontend && npm run build && sudo cp -r dist/* /var/www/html/

# 完整更新（包含后端）
sudo ./update_production.sh update

# 紧急回滚
sudo ./update_production.sh rollback

# 健康检查
curl http://localhost:8000/health/detailed
```

**现在你可以放心上线了！有了这套流程，随时修改内容都不是问题。**

有问题随时找我，我帮你搞定！ 🚀