# 🚀 生产环境更新工作流

## 📋 分支管理策略

```
main (生产环境)
  ↑
staging (预发布环境)
  ↑
develop (开发环境)
  ↑
feature/xxx (功能分支)
```

## 🔄 标准更新流程

### 1. 开发阶段
```bash
# 1. 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/新功能名称

# 2. 开发完成后合并到develop
git checkout develop
git merge feature/新功能名称
git push origin develop
```

### 2. 测试阶段
```bash
# 1. 合并到预发布环境
git checkout staging
git merge develop
git push origin staging

# 2. 部署到预发布环境测试
./deploy_staging.sh
```

### 3. 生产发布
```bash
# 1. 确认测试无误后合并到main
git checkout main
git merge staging
git tag -a v1.0.1 -m "版本发布说明"
git push origin main --tags

# 2. 部署到生产环境
sudo ./update_production.sh update
```

## ⚡ 快速热修复流程

### 紧急修复（hotfix）
```bash
# 1. 从main创建hotfix分支
git checkout main
git checkout -b hotfix/紧急修复描述

# 2. 修复代码并测试
# ... 修复代码 ...

# 3. 直接发布到生产环境
git checkout main
git merge hotfix/紧急修复描述
git tag -a v1.0.2 -m "紧急修复：修复内容描述"
git push origin main --tags

# 4. 立即部署
sudo ./update_production.sh update
```

## 🎯 不同类型更新的具体操作

### A. 前端内容更新（文案、图片、样式）

**特点：** 无需重启后端，风险低

```bash
# 1. 更新代码
git pull origin main

# 2. 仅构建前端
cd frontend
npm run build

# 3. 更新静态文件（零停机）
sudo cp -r dist/* /var/www/html/
sudo nginx -s reload

# 4. 验证更新
curl -I http://你的域名.com
```

### B. 后端功能更新（API修改、业务逻辑）

**特点：** 需要重启服务，中等风险

```bash
# 1. 完整更新流程
sudo ./update_production.sh update

# 2. 监控日志
sudo docker-compose logs -f backend
```

### C. 数据库结构更新（新增表、字段）

**特点：** 高风险，需要谨慎处理

```bash
# 1. 先在预发布环境测试
./deploy_staging.sh

# 2. 确认无误后生产环境部署
sudo ./update_production.sh update

# 3. 密切监控数据库性能
# 检查慢查询、锁等情况
```

### D. 配置文件更新（环境变量、第三方服务）

**特点：** 可能影响整个系统

```bash
# 1. 更新配置文件
sudo nano /var/www/tcm-platform/.env

# 2. 重启相关服务
sudo docker-compose restart backend

# 3. 健康检查
curl http://localhost:8000/health/detailed
```

## 🔧 实用更新命令

### 快速命令合集

```bash
# 查看当前版本
git describe --tags

# 查看待部署的更改
git log --oneline main..origin/main

# 检查系统状态
sudo ./update_production.sh health

# 创建手动备份
sudo ./update_production.sh backup

# 紧急回滚
sudo ./update_production.sh rollback
```

### 监控命令

```bash
# 实时日志
sudo docker-compose logs -f

# 系统资源
htop
df -h

# 数据库状态
sudo docker-compose exec db pg_stat_activity

# Nginx访问日志
sudo tail -f /var/log/nginx/access.log
```

## 🚨 故障处理预案

### 1. 更新失败处理

```bash
# 自动回滚
sudo ./update_production.sh rollback

# 手动检查
sudo docker-compose ps
sudo docker-compose logs backend

# 如果自动回滚失败
sudo docker-compose down
sudo docker-compose up -d
```

### 2. 数据库问题处理

```bash
# 检查数据库连接
sudo docker-compose exec backend python -c "from app.database import engine; print(engine.connect())"

# 回滚数据库迁移
sudo docker-compose exec backend alembic downgrade -1

# 重启数据库
sudo docker-compose restart db
```

### 3. 前端访问问题

```bash
# 检查Nginx配置
sudo nginx -t

# 重新加载Nginx
sudo nginx -s reload

# 检查静态文件权限
sudo chown -R www-data:www-data /var/www/html/
```

## 📊 更新清单模板

### 每次更新前检查

- [ ] **代码审查完成**
- [ ] **预发布环境测试通过**
- [ ] **数据库备份完成**
- [ ] **回滚方案准备就绪**
- [ ] **通知相关人员**
- [ ] **选择低峰期执行**

### 更新后验证

- [ ] **健康检查通过**
- [ ] **核心功能测试**
- [ ] **性能监控正常**
- [ ] **错误日志检查**
- [ ] **用户反馈收集**

## 📱 自动化发布（进阶）

### GitHub Actions配置

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      run: |
        ssh user@your-server 'cd /var/www/tcm-platform && sudo ./update_production.sh update'
```

### Webhook自动部署

```bash
# 设置webhook接收脚本
sudo nano /var/www/webhook-deploy.php
```

## 🎯 最佳实践

1. **永远在预发布环境先测试**
2. **选择用户活跃度低的时间更新**
3. **每次更新前创建完整备份**
4. **更新后及时监控系统状态**
5. **保持更新频率，避免累积大量更改**
6. **重要更新提前通知用户**

---

**记住：稳定性永远比新功能更重要！**