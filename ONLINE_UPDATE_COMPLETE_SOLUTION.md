# 🚀 线上更新完整解决方案

**版本：** v1.0.0  
**创建时间：** 2025-01-15  
**适用项目：** 中医健康服务平台

---

## 📖 方案概述

本方案提供了一套完整的**生产环境热更新系统**，包含：
- ⚡ 零停机部署
- 🔄 自动备份回滚  
- 🧪 多环境测试流程
- 📊 实时健康监控
- 🛡️ 安全保障机制

**核心优势：**
- 5分钟快速更新
- 用户零感知
- 失败自动回滚
- 操作简单安全

---

## 🎯 核心功能特性

### 1. **热更新能力**
```bash
# 前端内容更新（30秒）
git push → 自动构建 → 零停机更新

# 后端功能更新（2-5分钟）  
git push → 预发布测试 → 一键生产部署
```

### 2. **多环境管理**
```
开发环境 (develop) 
    ↓
预发布环境 (staging)
    ↓  
生产环境 (main)
```

### 3. **安全保障**
- 🔐 每次部署自动创建完整备份
- 🚨 健康检查失败自动回滚
- 📝 完整操作日志记录
- ⚡ 一键紧急回滚功能

---

## 🛠️ 核心文件说明

### 主要脚本文件

| 文件名 | 功能 | 使用场景 |
|--------|------|----------|
| `update_production.sh` | 生产环境热更新脚本 | 日常内容更新 |
| `deploy_staging.sh` | 预发布环境部署 | 重大更新前测试 |
| `.env.production` | 生产环境配置模板 | 首次部署配置 |

### 文档文件

| 文件名 | 内容 | 用途 |
|--------|------|------|
| `DEPLOYMENT_WORKFLOW.md` | 完整工作流程 | 开发团队参考 |
| `HOW_TO_UPDATE_ONLINE.md` | 快速操作手册 | 日常更新指南 |
| `PRODUCTION_CHECKLIST.md` | 生产环境检查清单 | 上线前检查 |

---

## ⚡ 快速更新操作

### A. 小改动（推荐 - 30秒完成）

**适用场景：** 前端文案、样式、图片修改

```bash
# 1. 本地修改并提交
git add .
git commit -m "更新：描述修改内容"
git push origin main

# 2. 服务器快速更新（单条命令）
ssh user@server "cd /var/www/tcm-platform && git pull && cd frontend && npm run build && sudo cp -r dist/* /var/www/html/ && sudo nginx -s reload"
```

### B. 功能更新（标准 - 2-5分钟）

**适用场景：** API修改、业务逻辑变更、数据库更新

```bash
# 1. 先在预发布环境测试
./deploy_staging.sh deploy
# 测试确认无误...

# 2. 一键部署到生产环境
sudo ./update_production.sh update
```

### C. 紧急修复（快速 - 1分钟）

**适用场景：** 线上bug紧急修复

```bash
# 1. 直接修复并推送
git add . && git commit -m "紧急修复：描述问题" && git push origin main

# 2. 立即热更新
sudo ./update_production.sh update
```

---

## 🎛️ 常用管理命令

### 系统状态检查
```bash
# 健康检查
curl http://你的域名.com/health/detailed

# 服务状态
sudo docker-compose ps

# 实时日志
sudo docker-compose logs -f backend
```

### 备份和回滚
```bash
# 手动备份
sudo ./update_production.sh backup

# 紧急回滚
sudo ./update_production.sh rollback

# 查看版本
git describe --tags
```

### 监控命令
```bash
# 访问日志
sudo tail -f /var/log/nginx/access.log

# 系统资源
htop && df -h

# 错误日志
sudo docker-compose logs backend | grep -i error
```

---

## 🚨 故障应急处理

### 1. 网站无法访问
```bash
# 快速诊断
sudo docker-compose ps
curl -I http://localhost

# 重启服务
sudo docker-compose restart

# 如果无效，立即回滚
sudo ./update_production.sh rollback
```

### 2. 数据库连接问题
```bash
# 检查数据库状态
sudo docker-compose exec db pg_isready

# 测试连接
sudo docker-compose exec backend python -c "from app.database import engine; print(engine.connect())"

# 重启数据库
sudo docker-compose restart db
```

### 3. 前端页面异常
```bash
# 检查静态文件
ls -la /var/www/html/

# 重新构建前端
cd frontend && npm run build && sudo cp -r dist/* /var/www/html/

# 检查nginx
sudo nginx -t && sudo nginx -s reload
```

---

## 📋 更新场景实战指南

### 场景1：修改首页文字

**需求：** 把首页标题从"中医健康平台"改为"专业中医健康服务平台"

```bash
# 1. 修改前端代码
vim frontend/src/views/HomePage.vue
# 找到标题，修改文字

# 2. 提交更改  
git add . && git commit -m "更新首页标题" && git push origin main

# 3. 服务器更新（30秒完成）
ssh user@server "cd /var/www/tcm-platform && git pull && cd frontend && npm run build && sudo cp -r dist/* /var/www/html/"
```

### 场景2：新增用户积分功能

**需求：** 为用户表增加积分字段，增加积分相关API

```bash
# 1. 修改数据模型
vim backend/app/models/user.py
# 添加：points = Column(Integer, default=0)

# 2. 生成数据库迁移
cd backend && alembic revision --autogenerate -m "添加用户积分字段"

# 3. 修改API
vim backend/app/api/users.py
# 添加积分相关接口

# 4. 修改前端页面
vim frontend/src/views/UserProfile.vue
# 添加积分显示

# 5. 提交所有更改
git add . && git commit -m "新增：用户积分功能" && git push origin main

# 6. 先在预发布环境测试
./deploy_staging.sh deploy
# 访问 http://localhost:3001 测试功能

# 7. 确认无误后部署生产环境
sudo ./update_production.sh update
```

### 场景3：修复支付回调bug

**需求：** 支付宝回调处理有bug，需要紧急修复

```bash
# 1. 直接在main分支修复
git checkout main
vim backend/app/api/reliable_payment.py
# 修复回调逻辑bug

# 2. 立即提交和部署
git add . && git commit -m "紧急修复：支付宝回调bug" && git push origin main
sudo ./update_production.sh update

# 3. 密切监控支付功能
curl http://localhost:8000/health/detailed
sudo docker-compose logs -f backend | grep -i payment
```

---

## 🔄 标准Git工作流程

### 分支管理策略
```
main (生产环境，只合并稳定代码)
  ↑
staging (预发布，用于最终测试)  
  ↑
develop (开发环境，日常开发)
  ↑
feature/* (功能分支，具体功能开发)
hotfix/* (热修复分支，紧急修复)
```

### 日常开发流程
```bash
# 1. 创建功能分支
git checkout develop
git checkout -b feature/用户积分系统

# 2. 开发完成后合并到develop
git checkout develop
git merge feature/用户积分系统
git push origin develop

# 3. 准备发布时合并到staging测试
git checkout staging  
git merge develop
git push origin staging
./deploy_staging.sh deploy

# 4. 测试通过后发布到生产环境
git checkout main
git merge staging
git tag -a v1.2.0 -m "新增用户积分系统"
git push origin main --tags
sudo ./update_production.sh update
```

---

## 📊 监控和日志

### 关键监控指标
```bash
# 系统健康状态
curl -s http://localhost:8000/health/detailed | python -m json.tool

# 服务运行状态  
sudo docker-compose ps

# 系统资源使用
free -m && df -h

# 数据库连接数
sudo docker-compose exec db psql -U tcm_user -d tcm_platform -c "SELECT count(*) FROM pg_stat_activity;"
```

### 日志文件位置
```bash
# 应用日志
sudo docker-compose logs backend
sudo docker-compose logs frontend

# Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# 系统日志
sudo journalctl -u docker -f

# 部署日志
tail -f /var/log/deployment.log
```

---

## 🛡️ 安全最佳实践

### 1. 更新前检查清单
- [ ] 代码审查完成
- [ ] 在预发布环境充分测试
- [ ] 数据库备份完成
- [ ] 选择低峰期执行
- [ ] 准备好回滚方案

### 2. 更新过程监控
- [ ] 实时监控系统资源
- [ ] 观察错误日志
- [ ] 检查关键功能是否正常
- [ ] 监控用户反馈

### 3. 更新后验证
- [ ] 健康检查通过
- [ ] 核心功能测试
- [ ] 性能指标正常
- [ ] 用户访问正常

---

## 🎯 常见问题FAQ

### Q1: 更新失败了怎么办？
```bash
# 自动回滚
sudo ./update_production.sh rollback

# 如果自动回滚失败，手动处理
sudo docker-compose down
sudo docker-compose up -d
```

### Q2: 数据库迁移失败怎么办？
```bash
# 回滚数据库迁移
sudo docker-compose exec backend alembic downgrade -1

# 检查迁移文件
sudo docker-compose exec backend alembic history
```

### Q3: 前端更新后显示还是旧内容？
```bash
# 清理浏览器缓存，重新构建前端
cd frontend && rm -rf dist && npm run build
sudo cp -r dist/* /var/www/html/
sudo nginx -s reload
```

### Q4: 如何查看当前运行的版本？
```bash
# Git版本信息
git describe --tags

# 应用版本信息（如果在代码中设置了）
curl http://localhost:8000/api/ | grep version
```

---

## 📚 相关文档索引

1. **[生产环境检查清单](./PRODUCTION_CHECKLIST.md)** - 上线前必读
2. **[部署工作流程](./DEPLOYMENT_WORKFLOW.md)** - 完整开发流程
3. **[快速更新手册](./HOW_TO_UPDATE_ONLINE.md)** - 日常操作指南
4. **[生产环境配置](./.env.production)** - 环境变量模板

---

## 💡 进阶功能

### 自动化部署（GitHub Actions）
```yaml
# .github/workflows/deploy.yml
name: Auto Deploy
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
        ssh deploy@server 'cd /var/www/tcm-platform && sudo ./update_production.sh update'
```

### 监控告警集成
```bash
# 可以集成的监控服务
- Sentry（错误追踪）
- Prometheus + Grafana（性能监控）
- 钉钉/企业微信（告警通知）
- 阿里云/腾讯云监控
```

---

## 🎉 总结

现在你拥有了一套**企业级的热更新系统**：

### ✅ 核心能力
- 🚀 **5分钟快速更新** - 前端30秒，后端5分钟
- 🔄 **零停机部署** - 用户完全无感知
- 🛡️ **安全保障** - 自动备份+一键回滚
- 📊 **完整监控** - 实时状态检查

### ✅ 操作简单
```bash
# 日常更新就这两步
git push origin main                    # 1. 推送代码  
sudo ./update_production.sh update     # 2. 更新部署
```

### ✅ 风险可控
- 失败自动回滚
- 完整备份策略  
- 实时健康监控
- 多环境测试验证

**现在可以放心上线了！有了这套方案，线上修改内容比本地开发还简单。** 🎯

---

**文档版本：** v1.0.0  
**最后更新：** 2025-01-15  
**维护人员：** Claude Code Assistant

*如有问题或建议，请及时更新本文档。*