#!/bin/bash
# 数据恢复脚本

set -e

# 配置
BACKUP_DIR="/app/backups"
DB_NAME="tcm_platform"
DB_USER="tcm_user"
DB_HOST="db"

# 检查参数
if [ $# -eq 0 ]; then
    echo "用法: $0 <backup_timestamp>"
    echo "示例: $0 20241201_120000"
    echo ""
    echo "可用备份文件:"
    ls -la "$BACKUP_DIR"/backup_*.sql.gz 2>/dev/null | awk '{print $9}' | sed 's/.*backup_//' | sed 's/.sql.gz//' || echo "无备份文件"
    exit 1
fi

TIMESTAMP=$1
BACKUP_FILE="$BACKUP_DIR/backup_${TIMESTAMP}.sql.gz"
UPLOADS_BACKUP="$BACKUP_DIR/uploads_${TIMESTAMP}.tar.gz"

# 检查备份文件是否存在
if [ ! -f "$BACKUP_FILE" ]; then
    echo "错误: 备份文件不存在 - $BACKUP_FILE"
    exit 1
fi

echo "开始恢复数据 - $(date)"
echo "备份文件: $BACKUP_FILE"

# 确认恢复操作
read -p "确定要恢复数据吗？这将覆盖当前数据库! (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "恢复操作已取消"
    exit 0
fi

# 1. 恢复数据库
echo "恢复数据库..."
gunzip -c "$BACKUP_FILE" | PGPASSWORD="${DB_PASSWORD}" psql \
    -h "$DB_HOST" \
    -U "$DB_USER" \
    -d postgres  # 连接到默认数据库执行创建操作

if [ $? -eq 0 ]; then
    echo "数据库恢复完成"
else
    echo "数据库恢复失败!"
    exit 1
fi

# 2. 恢复上传文件
if [ -f "$UPLOADS_BACKUP" ]; then
    echo "恢复上传文件..."
    
    # 备份现有上传文件
    if [ -d "/app/uploads" ]; then
        mv "/app/uploads" "/app/uploads_backup_$(date +%Y%m%d_%H%M%S)"
        echo "现有上传文件已备份"
    fi
    
    # 恢复上传文件
    tar -xzf "$UPLOADS_BACKUP" -C /app/
    
    if [ $? -eq 0 ]; then
        echo "上传文件恢复完成"
    else
        echo "上传文件恢复失败!"
        exit 1
    fi
else
    echo "上传文件备份不存在，跳过恢复"
fi

echo "数据恢复完成 - $(date)"

# 记录恢复操作
cat >> "$BACKUP_DIR/restore.log" << EOF
$(date): 数据恢复完成
- 恢复时间戳: $TIMESTAMP
- 数据库备份: $(basename "$BACKUP_FILE")
- 上传文件备份: $(basename "$UPLOADS_BACKUP")
EOF

echo "恢复日志已更新"
echo ""
echo "建议重启应用服务以确保数据一致性"