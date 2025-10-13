# Git历史清理指南

## ⚠️ 发现的问题

通过检查发现，当前Git仓库中包含了不应该提交的文件：

### 1. Python缓存文件
- `__pycache__/` 目录
- `*.pyc` 编译文件
- 这些文件会增加仓库大小，且可能包含代码路径信息

### 2. 数据库文件（如果有）
- `*.db` SQLite数据库文件可能包含敏感数据

---

## 🔧 清理方案

### 方案A: 保守清理（推荐新手）

**只清理未来的提交，不改变历史**

```bash
# 1. 更新.gitignore
cat >> .gitignore << EOF

# Python缓存
__pycache__/
*.py[cod]
*.pyc
*.pyo
*.pyd

# 数据库
*.db
*.sqlite
*.sqlite3

# 环境变量
.env
.env.local
.env.*.local
EOF

# 2. 从Git索引移除（但保留本地文件）
git rm -r --cached backend/app/**/__pycache__
git rm -r --cached backend/app/**/*.pyc
git rm --cached backend/*.db 2>/dev/null || true

# 3. 提交清理
git add .gitignore
git commit -m "🧹 清理：移除缓存文件并更新gitignore"
```

---

### 方案B: 完全清理历史（高级，不可逆！）

**⚠️ 警告**: 这会重写Git历史，团队协作需谨慎！

```bash
# 备份当前仓库
cd ..
cp -r 999 999_backup

cd 999

# 使用git filter-repo清理（推荐）
# 先安装: pip install git-filter-repo

git filter-repo --path backend/app --path-glob '**/__pycache__' --invert-paths
git filter-repo --path-glob '*.pyc' --invert-paths
git filter-repo --path-glob '*.db' --invert-paths

# 或使用BFG Repo-Cleaner（更快）
# 下载: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-folders __pycache__ .
java -jar bfg.jar --delete-files '*.pyc' .
java -jar bfg.jar --delete-files '*.db' .

git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 强制推送（如果有远程仓库）
# git push origin --force --all
```

---

## ✅ 验证清理效果

```bash
# 检查仓库大小
du -sh .git

# 检查是否还有缓存文件
git log --all --name-only --pretty=format: | grep -E "__pycache__|\.pyc" | wc -l

# 查看.gitignore
cat .gitignore
```

---

## 📋 .gitignore完整模板

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 环境变量
.env
.env.local
.env.*.local
backend/.env

# 数据库
*.db
*.sqlite
*.sqlite3
backend/*.db
backend/*.db.backup*

# 日志
*.log
logs/

# 密钥和证书
*.pem
*.key
*.crt
*.p12
*.pfx

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# 前端
node_modules/
frontend/dist/
frontend/node_modules/
mobile/dist/
mobile/node_modules/
mobile/unpackage/

# 备份
*.backup
*.bak
*.tmp
```

---

## 🚀 推荐执行步骤

1. **立即执行方案A**（安全，可逆）
2. 验证本地开发正常
3. 如果需要完全清理历史，再执行方案B
4. 推送到远程仓库（如果有）

---

## ⚠️ 重要提醒

- `.env` 文件**永远不要**提交到Git
- 敏感配置使用环境变量或密钥管理服务
- 定期检查Git历史，避免泄露
- 使用 `git-secrets` 工具预防敏感信息提交

```bash
# 安装git-secrets
brew install git-secrets  # macOS
# 或从源码安装: https://github.com/awslabs/git-secrets

# 配置检查规则
git secrets --register-aws
git secrets --add 'SECRET_KEY.*'
git secrets --add 'PASSWORD.*'
```
