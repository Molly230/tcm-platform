#!/bin/bash
# 数据备份脚本

set -e  # 遇到错误立即退出

# 配置
BACKUP_DIR="/app/backups"
DB_NAME="tcm_platform"
DB_USER="tcm_user"
DB_HOST="db"
RETENTION_DAYS=30

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 生成备份文件名
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_${TIMESTAMP}.sql"
UPLOADS_BACKUP="$BACKUP_DIR/uploads_${TIMESTAMP}.tar.gz"

echo "开始备份 - $(date)"

# 1. 备份数据库
echo "备份数据库..."
PGPASSWORD="${DB_PASSWORD}" pg_dump \
    -h "$DB_HOST" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --verbose \
    --clean \
    --if-exists \
    --create \
    > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "数据库备份完成: $BACKUP_FILE"
    # 压缩备份文件
    gzip "$BACKUP_FILE"
    BACKUP_FILE="${BACKUP_FILE}.gz"
    echo "备份文件已压缩: $BACKUP_FILE"
else
    echo "数据库备份失败!"
    exit 1
fi

# 2. 备份上传文件
echo "备份上传文件..."
if [ -d "/app/uploads" ]; then
    tar -czf "$UPLOADS_BACKUP" -C /app uploads/
    if [ $? -eq 0 ]; then
        echo "上传文件备份完成: $UPLOADS_BACKUP"
    else
        echo "上传文件备份失败!"
        exit 1
    fi
else
    echo "上传目录不存在，跳过文件备份"
fi

# 3. 清理旧备份文件
echo "清理 ${RETENTION_DAYS} 天前的备份文件..."
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +${RETENTION_DAYS} -delete
find "$BACKUP_DIR" -name "uploads_*.tar.gz" -mtime +${RETENTION_DAYS} -delete

echo "备份完成 - $(date)"

# 4. 备份信息记录
cat >> "$BACKUP_DIR/backup.log" << EOF
$(date): 备份完成
- 数据库备份: $(basename "$BACKUP_FILE")
- 上传文件备份: $(basename "$UPLOADS_BACKUP")
- 备份大小: $(du -sh "$BACKUP_FILE" | cut -f1) / $(du -sh "$UPLOADS_BACKUP" | cut -f1)
EOF

echo "备份日志已更新"