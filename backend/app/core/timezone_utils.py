"""
时区处理工具
统一项目中的时间处理方式
"""
from datetime import datetime, timezone
import pytz


def utc_now() -> datetime:
    """获取当前UTC时间，带时区信息"""
    return datetime.now(timezone.utc)


def beijing_now() -> datetime:
    """获取当前北京时间"""
    beijing_tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(beijing_tz)


def to_utc(dt: datetime) -> datetime:
    """将时间转换为UTC时间"""
    if dt.tzinfo is None:
        # 如果没有时区信息，假设为UTC时间
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_beijing(dt: datetime) -> datetime:
    """将时间转换为北京时间"""
    if dt.tzinfo is None:
        # 如果没有时区信息，假设为UTC时间
        dt = dt.replace(tzinfo=timezone.utc)
    
    beijing_tz = pytz.timezone('Asia/Shanghai')
    return dt.astimezone(beijing_tz)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化时间显示"""
    if dt is None:
        return ""
    return dt.strftime(format_str)


def format_datetime_with_tz(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
    """格式化时间显示，包含时区"""
    if dt is None:
        return ""
    return dt.strftime(format_str)