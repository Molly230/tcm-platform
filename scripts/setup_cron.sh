#!/bin/bash
# 设置定时备份任务

echo "设置定时备份任务..."

# 创建crontab配置文件
cat > /tmp/tcm_cron << 'EOF'
# 中医健康服务平台 - 定时任务

# 每天凌晨2点执行数据备份
0 2 * * * /app/scripts/backup.sh >> /app/logs/backup.log 2>&1

# 每小时执行一次系统监控
0 * * * * /usr/bin/python3 /app/scripts/monitor.py >> /app/logs/monitor_cron.log 2>&1

# 每天凌晨1点清理过期日志文件（保留30天）
0 1 * * * find /app/logs -name "*.log*" -mtime +30 -delete

# 每周日凌晨3点清理临时文件
0 3 * * 0 find /tmp -name "*.tmp" -mtime +7 -delete

EOF

# 安装crontab
crontab /tmp/tcm_cron

# 启动cron服务
service cron start || systemctl start cron || echo "请手动启动cron服务"

echo "定时任务设置完成"
echo "当前crontab任务:"
crontab -l

# 清理临时文件
rm -f /tmp/tcm_cron