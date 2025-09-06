"""
日志系统配置
"""
import os
import logging
import logging.handlers
from datetime import datetime
from typing import Optional
from app.core.config import settings

class AdminLogger:
    """管理后台专用日志器"""
    
    def __init__(self):
        self.logger = logging.getLogger("admin")
        self.logger.setLevel(logging.INFO)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        # 创建日志目录
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # 文件处理器 - 按日期轮转
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_dir, "admin.log"),
            when="midnight",
            interval=1,
            backupCount=30,  # 保留30天的日志
            encoding='utf-8'
        )
        file_handler.suffix = "%Y-%m-%d"
        
        # 错误日志单独记录
        error_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_dir, "admin_error.log"),
            when="midnight", 
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        error_handler.suffix = "%Y-%m-%d"
        error_handler.setLevel(logging.ERROR)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        if settings.DEBUG:
            self.logger.addHandler(console_handler)
    
    def log_admin_action(self, user_id: int, username: str, action: str, 
                        target: Optional[str] = None, details: Optional[str] = None,
                        ip_address: Optional[str] = None):
        """记录管理员操作"""
        message = f"管理员操作 - 用户ID:{user_id} 用户名:{username} 操作:{action}"
        if target:
            message += f" 目标:{target}"
        if details:
            message += f" 详情:{details}"
        if ip_address:
            message += f" IP:{ip_address}"
        
        self.logger.info(message)
    
    def log_login(self, user_id: int, username: str, success: bool, 
                 ip_address: Optional[str] = None, reason: Optional[str] = None):
        """记录登录尝试"""
        status = "成功" if success else "失败"
        message = f"登录{status} - 用户ID:{user_id} 用户名:{username}"
        if ip_address:
            message += f" IP:{ip_address}"
        if reason:
            message += f" 原因:{reason}"
        
        if success:
            self.logger.info(message)
        else:
            self.logger.warning(message)
    
    def log_file_upload(self, user_id: int, username: str, filename: str, 
                       file_size: int, file_type: str, ip_address: Optional[str] = None):
        """记录文件上传"""
        message = (f"文件上传 - 用户ID:{user_id} 用户名:{username} "
                  f"文件名:{filename} 大小:{file_size}字节 类型:{file_type}")
        if ip_address:
            message += f" IP:{ip_address}"
        
        self.logger.info(message)
    
    def log_data_export(self, user_id: int, username: str, export_type: str,
                       record_count: int, ip_address: Optional[str] = None):
        """记录数据导出"""
        message = (f"数据导出 - 用户ID:{user_id} 用户名:{username} "
                  f"类型:{export_type} 记录数:{record_count}")
        if ip_address:
            message += f" IP:{ip_address}"
        
        self.logger.info(message)
    
    def log_error(self, user_id: int, username: str, error: str, 
                 context: Optional[str] = None, ip_address: Optional[str] = None):
        """记录错误"""
        message = f"系统错误 - 用户ID:{user_id} 用户名:{username} 错误:{error}"
        if context:
            message += f" 上下文:{context}"
        if ip_address:
            message += f" IP:{ip_address}"
        
        self.logger.error(message)
    
    def log_system_event(self, event: str, details: Optional[str] = None):
        """记录系统事件"""
        message = f"系统事件 - {event}"
        if details:
            message += f" 详情:{details}"
        
        self.logger.info(message)

# 创建全局日志实例
admin_logger = AdminLogger()

def get_client_ip(request) -> str:
    """获取客户端IP地址"""
    # 检查常见的代理头
    forwarded_for = getattr(request, 'headers', {}).get('x-forwarded-for')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    
    real_ip = getattr(request, 'headers', {}).get('x-real-ip')
    if real_ip:
        return real_ip
    
    # 从客户端信息获取
    client = getattr(request, 'client', None)
    if client and hasattr(client, 'host'):
        return client.host
    
    return "unknown"

def log_admin_action(user, action: str, target: Optional[str] = None, 
                    details: Optional[str] = None, request=None):
    """便捷的管理员操作日志记录函数"""
    ip_address = get_client_ip(request) if request else None
    admin_logger.log_admin_action(
        user_id=user.id,
        username=user.username,
        action=action,
        target=target,
        details=details,
        ip_address=ip_address
    )

def log_file_upload(user, filename: str, file_size: int, file_type: str, request=None):
    """便捷的文件上传日志记录函数"""
    ip_address = get_client_ip(request) if request else None
    admin_logger.log_file_upload(
        user_id=user.id,
        username=user.username,
        filename=filename,
        file_size=file_size,
        file_type=file_type,
        ip_address=ip_address
    )

def log_data_export(user, export_type: str, record_count: int, request=None):
    """便捷的数据导出日志记录函数"""
    ip_address = get_client_ip(request) if request else None
    admin_logger.log_data_export(
        user_id=user.id,
        username=user.username,
        export_type=export_type,
        record_count=record_count,
        ip_address=ip_address
    )