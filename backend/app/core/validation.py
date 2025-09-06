"""
输入验证工具
"""
import re
from typing import Optional


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    验证密码强度
    
    要求:
    - 至少8个字符
    - 至少包含一个大写字母
    - 至少包含一个小写字母
    - 至少包含一个数字
    - 至少包含一个特殊字符
    """
    if len(password) < 8:
        return False, "密码长度至少8个字符"
    
    if len(password) > 128:
        return False, "密码长度不能超过128个字符"
    
    if not re.search(r"[a-z]", password):
        return False, "密码必须包含至少一个小写字母"
    
    if not re.search(r"[A-Z]", password):
        return False, "密码必须包含至少一个大写字母"
    
    if not re.search(r"\d", password):
        return False, "密码必须包含至少一个数字"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "密码必须包含至少一个特殊字符 (!@#$%^&*(),.?\":{}|<>)"
    
    # 检查常见弱密码
    weak_passwords = [
        "12345678", "password", "admin123", "qwerty123", 
        "abc123456", "123456789", "password123", "admin1234"
    ]
    
    if password.lower() in weak_passwords:
        return False, "密码过于简单，请使用更复杂的密码"
    
    return True, "密码强度符合要求"


def validate_email(email: str) -> tuple[bool, str]:
    """验证邮箱格式"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not email:
        return False, "邮箱不能为空"
    
    if len(email) > 254:
        return False, "邮箱长度不能超过254个字符"
    
    if not re.match(email_pattern, email):
        return False, "邮箱格式不正确"
    
    return True, "邮箱格式正确"


def validate_phone(phone: str) -> tuple[bool, str]:
    """验证手机号格式（中国大陆）"""
    if not phone:
        return True, "手机号为空（可选）"
    
    # 中国大陆手机号正则
    phone_pattern = r'^1[3-9]\d{9}$'
    
    if not re.match(phone_pattern, phone):
        return False, "手机号格式不正确"
    
    return True, "手机号格式正确"


def validate_username(username: str) -> tuple[bool, str]:
    """验证用户名"""
    if not username:
        return False, "用户名不能为空"
    
    if len(username) < 3:
        return False, "用户名长度至少3个字符"
    
    if len(username) > 20:
        return False, "用户名长度不能超过20个字符"
    
    # 用户名只能包含字母、数字、下划线
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "用户名只能包含字母、数字和下划线"
    
    # 不能全是数字
    if username.isdigit():
        return False, "用户名不能全是数字"
    
    # 禁用的用户名
    forbidden_usernames = [
        "admin", "administrator", "root", "system", "test", 
        "user", "guest", "null", "undefined", "api"
    ]
    
    if username.lower() in forbidden_usernames:
        return False, "该用户名不可用"
    
    return True, "用户名格式正确"


def sanitize_string(input_str: str, max_length: Optional[int] = None) -> str:
    """清理字符串输入"""
    if not input_str:
        return ""
    
    # 去除首尾空格
    cleaned = input_str.strip()
    
    # 移除潜在的HTML标签
    cleaned = re.sub(r'<[^>]+>', '', cleaned)
    
    # 移除SQL注入常用字符（基础防护）
    dangerous_patterns = [
        r"'", r'"', r';', r'--', r'/\*', r'\*/',
        r'\bUNION\b', r'\bSELECT\b', r'\bINSERT\b', 
        r'\bUPDATE\b', r'\bDELETE\b', r'\bDROP\b'
    ]
    
    for pattern in dangerous_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # 限制长度
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned


def validate_full_name(full_name: str) -> tuple[bool, str]:
    """验证真实姓名"""
    if not full_name:
        return True, "姓名为空（可选）"
    
    if len(full_name) > 50:
        return False, "姓名长度不能超过50个字符"
    
    # 只允许中文、英文字母和空格
    if not re.match(r'^[\u4e00-\u9fa5a-zA-Z\s]+$', full_name):
        return False, "姓名只能包含中文、英文字母和空格"
    
    return True, "姓名格式正确"