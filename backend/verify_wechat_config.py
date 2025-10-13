"""
微信支付生产环境配置验证工具
验证所有配置项是否正确，并提供修复建议
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from typing import Dict, List, Tuple


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")


def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")


def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")


def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")


def check_env_config() -> Tuple[bool, List[str], List[str]]:
    """检查环境变量配置"""
    print_header("步骤1: 验证环境变量配置")

    errors = []
    warnings = []

    # 读取.env文件
    env_file = "backend/.env"
    if not os.path.exists(env_file):
        env_file = ".env"

    if not os.path.exists(env_file):
        print_error(f".env 文件不存在")
        return False, ["缺少.env配置文件"], []

    with open(env_file, 'r', encoding='utf-8') as f:
        env_content = f.read()

    # 检查各项配置
    checks = [
        {
            'name': 'WECHAT_APP_ID',
            'pattern': r'WECHAT_APP_ID=(\S+)',
            'validate': lambda v: v.startswith('wx') and len(v) == 18,
            'error_msg': '微信AppID格式错误（应为wx开头的18位字符）'
        },
        {
            'name': 'WECHAT_MCH_ID',
            'pattern': r'WECHAT_MCH_ID=(\S+)',
            'validate': lambda v: v.isdigit() and len(v) == 10,
            'error_msg': '商户号格式错误（应为10位数字）'
        },
        {
            'name': 'WECHAT_API_KEY',
            'pattern': r'WECHAT_API_KEY=(\S+)',
            'validate': lambda v: len(v) == 32,
            'error_msg': 'API密钥长度错误（必须为32位）'
        },
        {
            'name': 'WECHAT_NOTIFY_URL',
            'pattern': r'WECHAT_NOTIFY_URL=(\S+)',
            'validate': lambda v: v.startswith('https://') and 'wechat-pay/notify' in v,
            'error_msg': '回调URL格式错误（必须HTTPS且路径为/api/wechat-pay/notify）'
        },
        {
            'name': 'WECHAT_H5_DOMAIN',
            'pattern': r'WECHAT_H5_DOMAIN=(\S+)',
            'validate': lambda v: '.' in v and not v.startswith('http'),
            'error_msg': 'H5域名格式错误（不应包含http://前缀）'
        },
        {
            'name': 'WECHAT_MOCK_MODE',
            'pattern': r'WECHAT_MOCK_MODE=(\S+)',
            'validate': lambda v: v.lower() in ['true', 'false'],
            'error_msg': '模拟模式开关值错误（应为true或false）'
        }
    ]

    config_values = {}

    for check in checks:
        match = re.search(check['pattern'], env_content)
        if not match:
            errors.append(f"缺少配置项: {check['name']}")
            print_error(f"缺少配置: {check['name']}")
            continue

        value = match.group(1).split('#')[0].strip()
        config_values[check['name']] = value

        if not check['validate'](value):
            errors.append(f"{check['name']}: {check['error_msg']}")
            print_error(f"{check['name']}: {check['error_msg']}")
            print_info(f"  当前值: {value}")
        else:
            # 部分隐藏敏感信息
            if check['name'] == 'WECHAT_API_KEY':
                display_value = value[:8] + '*' * 16 + value[-8:]
            elif check['name'] == 'WECHAT_APP_ID':
                display_value = value[:8] + '***'
            else:
                display_value = value
            print_success(f"{check['name']}: {display_value}")

    # 检查模拟模式警告
    if config_values.get('WECHAT_MOCK_MODE', 'true').lower() == 'true':
        warnings.append("当前处于模拟模式，生产环境请设置 WECHAT_MOCK_MODE=false")
        print_warning("当前处于模拟模式")
    else:
        print_success("已启用真实支付模式")

    return len(errors) == 0, errors, warnings


def check_wechat_platform_config():
    """提示检查微信商户平台配置"""
    print_header("步骤2: 微信商户平台配置检查清单")

    checklist = [
        {
            'item': '1. 登录微信支付商户平台',
            'url': 'https://pay.weixin.qq.com/',
            'desc': '使用商户管理员账号登录'
        },
        {
            'item': '2. 配置API密钥',
            'path': '账户中心 > API安全 > API密钥',
            'desc': '设置32位随机字符串，与.env中的WECHAT_API_KEY一致'
        },
        {
            'item': '3. 配置支付回调域名',
            'path': '产品中心 > 开发配置 > 支付配置',
            'desc': '添加授权域名: tcmlife.top'
        },
        {
            'item': '4. 配置H5支付域名（如需H5支付）',
            'path': '产品中心 > H5支付 > 开通配置',
            'desc': '添加授权域名: tcmlife.top'
        },
        {
            'item': '5. 确认支付产品已开通',
            'path': '产品中心 > 我的产品',
            'desc': '确认Native支付/H5支付/JSAPI支付已开通'
        }
    ]

    print("请手动检查以下配置项：\n")
    for check in checklist:
        print(f"{Colors.BOLD}{check['item']}{Colors.END}")
        if 'url' in check:
            print(f"  访问: {Colors.BLUE}{check['url']}{Colors.END}")
        if 'path' in check:
            print(f"  路径: {Colors.YELLOW}{check['path']}{Colors.END}")
        print(f"  说明: {check['desc']}\n")

    print_warning("以上配置必须在微信商户平台完成，否则真实支付将失败")


def check_server_requirements():
    """检查服务器环境要求"""
    print_header("步骤3: 服务器环境要求")

    requirements = [
        "✓ 服务器必须有公网IP或域名",
        "✓ 回调URL必须支持HTTPS（微信要求）",
        "✓ 防火墙允许微信服务器访问回调接口",
        "✓ 确保端口8001（或Nginx反向代理端口）对外开放",
        "✓ 域名已正确解析到服务器IP",
        "✓ SSL证书有效且未过期"
    ]

    print("生产环境部署前，请确认：\n")
    for req in requirements:
        print(f"  {req}")

    print(f"\n{Colors.YELLOW}测试回调URL可访问性：{Colors.END}")
    print(f"  在服务器上运行：")
    print(f"  {Colors.BLUE}curl -I https://tcmlife.top/api/wechat-pay/notify{Colors.END}")
    print(f"  应返回 HTTP/1.1 405 Method Not Allowed（因为应该用POST）")


def generate_deploy_script():
    """生成部署脚本"""
    print_header("步骤4: 生产环境部署步骤")

    steps = [
        ("1. 停止后端服务", "supervisorctl stop tcm_backend  # 或使用你的服务管理工具"),
        ("2. 备份当前配置", "cp backend/.env backend/.env.backup"),
        ("3. 更新代码", "git pull origin main"),
        ("4. 修改配置切换到生产模式", "编辑 backend/.env，设置 WECHAT_MOCK_MODE=false"),
        ("5. 重启后端服务", "supervisorctl start tcm_backend"),
        ("6. 检查服务日志", "tail -f backend/logs/app.log  # 查看是否有错误"),
        ("7. 运行验证测试", "python backend/test_wechat_pay.py"),
        ("8. 小额真实交易测试", "用0.01元订单测试真实支付流程")
    ]

    print("部署步骤：\n")
    for step, cmd in steps:
        print(f"{Colors.BOLD}{step}{Colors.END}")
        print(f"  {Colors.BLUE}{cmd}{Colors.END}\n")


def main():
    """主函数"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("=" * 70)
    print("     微信支付生产环境配置验证工具")
    print("=" * 70)
    print(f"{Colors.END}\n")

    # 检查环境变量配置
    success, errors, warnings = check_env_config()

    if not success:
        print(f"\n{Colors.RED}{'=' * 70}{Colors.END}")
        print(f"{Colors.RED}配置验证失败！请修复以下错误：{Colors.END}")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print(f"{Colors.RED}{'=' * 70}{Colors.END}\n")
        sys.exit(1)

    if warnings:
        print(f"\n{Colors.YELLOW}{'=' * 70}{Colors.END}")
        print(f"{Colors.YELLOW}警告信息：{Colors.END}")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
        print(f"{Colors.YELLOW}{'=' * 70}{Colors.END}\n")

    # 微信商户平台配置清单
    check_wechat_platform_config()

    # 服务器环境要求
    check_server_requirements()

    # 部署步骤
    generate_deploy_script()

    # 最终总结
    print_header("验证完成")
    print_success("环境变量配置验证通过")
    print_info("请按照上述清单完成微信商户平台配置")
    print_info("部署到生产环境前，请确认所有配置项")

    print(f"\n{Colors.BOLD}下一步操作：{Colors.END}")
    print(f"  1. 完成微信商户平台配置")
    print(f"  2. 启动后端服务测试")
    print(f"  3. 运行: python backend/test_wechat_pay.py")
    print(f"  4. 确认模拟支付正常后，修改 WECHAT_MOCK_MODE=false")
    print(f"  5. 进行小额真实支付测试\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}验证已取消{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}验证过程出错: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
