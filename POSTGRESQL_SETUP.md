# PostgreSQL生产环境配置指南

## 🚀 快速配置（阿里云RDS/自建服务器）

### 1. 安装PostgreSQL（如果是自建服务器）

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib -y

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib -y
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. 创建数据库和用户

```bash
# 切换到postgres用户
sudo -u postgres psql

# 在PostgreSQL命令行中执行：
CREATE DATABASE tcm_platform;
CREATE USER tcm_user WITH PASSWORD '你的强密码_改这里';
ALTER USER tcm_user WITH SUPERUSER;  -- 仅开发环境，生产环境用下面的权限
GRANT ALL PRIVILEGES ON DATABASE tcm_platform TO tcm_user;
\q
```

**生产环境权限（更安全）**:
```sql
-- 生产环境建议的最小权限
GRANT CONNECT ON DATABASE tcm_platform TO tcm_user;
GRANT CREATE ON DATABASE tcm_platform TO tcm_user;
\c tcm_platform
GRANT ALL ON SCHEMA public TO tcm_user;
```

### 3. 配置PostgreSQL远程访问（如果需要）

编辑 `/etc/postgresql/14/main/postgresql.conf`:
```conf
listen_addresses = '*'
```

编辑 `/etc/postgresql/14/main/pg_hba.conf`:
```conf
# 允许所有IP访问（仅开发环境）
host    all             all             0.0.0.0/0               md5

# 生产环境应该限制IP
host    all             all             你的服务器IP/32         md5
```

重启PostgreSQL:
```bash
sudo systemctl restart postgresql
```

---

## 📝 更新.env配置

在 `backend/.env` 中添加/修改：

```ini
# 生产环境 - PostgreSQL
DATABASE_URL=postgresql://tcm_user:你的强密码@localhost:5432/tcm_platform

# 如果是阿里云RDS
DATABASE_URL=postgresql://tcm_user:你的密码@rm-xxxxxx.mysql.rds.aliyuncs.com:5432/tcm_platform
```

**重要**: 记得修改密码！

---

## 🔄 数据迁移

### 从SQLite迁移到PostgreSQL

```bash
cd backend

# 1. 确保已安装依赖
pip install psycopg2-binary

# 2. 运行数据库迁移
alembic upgrade head

# 3. 重新创建管理员（如果需要）
python ../scripts/create_admin.py

# 4. 初始化数据（如果需要）
python ../scripts/seed_data.py
```

---

## ✅ 验证配置

```bash
cd backend
python -c "from app.database import engine; print('数据库连接成功:', engine.url)"
```

如果输出包含 `postgresql://`，说明配置成功！

---

## 🔐 安全建议

1. **强密码**: 使用至少16位随机密码
2. **防火墙**: 只开放必要的端口（5432）
3. **SSL连接**: 生产环境启用SSL
4. **定期备份**: 配置自动备份

### 配置SSL连接（生产环境必需）

```ini
DATABASE_URL=postgresql://tcm_user:密码@host:5432/tcm_platform?sslmode=require
```

---

## 📊 性能优化

编辑 `postgresql.conf`:
```conf
# 根据服务器内存调整
shared_buffers = 256MB          # 服务器内存的25%
effective_cache_size = 1GB      # 服务器内存的50-75%
work_mem = 16MB
maintenance_work_mem = 128MB
max_connections = 100
```

重启生效:
```bash
sudo systemctl restart postgresql
```

---

## 🆘 常见问题

### 1. 连接被拒绝
检查PostgreSQL是否运行:
```bash
sudo systemctl status postgresql
```

### 2. 密码认证失败
检查 `pg_hba.conf` 是否配置了 `md5` 认证

### 3. 权限不足
确保用户有足够权限:
```sql
ALTER USER tcm_user WITH SUPERUSER;
```

---

## 📦 阿里云RDS快速配置

1. 登录阿里云控制台
2. 创建PostgreSQL实例（建议11+版本）
3. 配置白名单（添加服务器IP）
4. 创建数据库 `tcm_platform`
5. 获取连接地址，更新.env

```ini
DATABASE_URL=postgresql://用户名:密码@rm-xxxxx.pg.rds.aliyuncs.com:5432/tcm_platform
```

**完成！** 🎉
