"""
日志配置模块
"""
import logging
import logging.handlers
import os
from pathlib import Path

def setup_logging():
    """配置应用日志"""
    
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # 清除现有的处理器
    root_logger.handlers = []
    
    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 应用日志文件（按日期轮转）
    app_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_dir / "app.log",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)
    root_logger.addHandler(app_handler)
    
    # 错误日志文件
    error_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "error.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # 数据库日志
    db_logger = logging.getLogger("sqlalchemy")
    db_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "database.log",
        maxBytes=10*1024*1024,
        backupCount=3,
        encoding="utf-8"
    )
    db_handler.setLevel(logging.WARNING)
    db_handler.setFormatter(formatter)
    db_logger.addHandler(db_handler)
    
    # 支付日志
    payment_logger = logging.getLogger("payment")
    payment_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "payment.log",
        maxBytes=5*1024*1024,
        backupCount=10,
        encoding="utf-8"
    )
    payment_handler.setLevel(logging.INFO)
    payment_handler.setFormatter(formatter)
    payment_logger.addHandler(payment_handler)
    
    # 安全日志
    security_logger = logging.getLogger("security")
    security_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "security.log",
        maxBytes=5*1024*1024,
        backupCount=10,
        encoding="utf-8"
    )
    security_handler.setLevel(logging.WARNING)
    security_handler.setFormatter(formatter)
    security_logger.addHandler(security_handler)
    
    logging.info("日志系统初始化完成")