"""
可靠的支付服务 - 模拟支付版本
简单、安全、可靠，适合开发测试
"""
import logging
from typing import Dict, Optional
from decimal import Decimal
import time
import uuid

logger = logging.getLogger(__name__)

class ReliablePayService:
    """基于模拟的可靠支付服务"""
    
    def __init__(self):
        # 模拟支付配置
        self.mock_mode = True
        logger.info("支付服务初始化完成 - 模拟支付模式")
        
    def create_payment(self, order_id: str, amount: Decimal, subject: str, 
                      payment_method: str = 'alipay_qr') -> Dict:
        """
        创建支付订单
        
        Args:
            order_id: 订单号
            amount: 金额（元）
            subject: 商品描述
            payment_method: 支付方式 alipay_qr/wechat/alipay
        
        Returns:
            支付结果
        """
        try:
            # 生成唯一的支付ID
            charge_id = f"mock_charge_{int(time.time())}_{uuid.uuid4().hex[:8]}"
            
            # 根据支付方式生成不同的支付URL
            if payment_method == 'alipay_qr':
                # 支付宝二维码
                payment_url = f"https://qr.alipay.com/mock/{charge_id}?amount={amount}&order={order_id}"
            elif payment_method == 'wechat':
                # 微信二维码
                payment_url = f"weixin://wxpay/bizpayurl?mock_id={charge_id}&amount={amount}&order={order_id}"
            else:
                # 支付宝网页支付
                payment_url = f"https://openapi.alipaydev.com/gateway.do?mock_id={charge_id}&amount={amount}&order={order_id}"
            
            logger.info(f"模拟支付创建成功: {order_id}, charge_id: {charge_id}")
            
            return {
                'success': True,
                'payment_url': payment_url,
                'charge_id': charge_id,
                'payment_method': payment_method,
                'mock_mode': True
            }
            
        except Exception as e:
            logger.error(f"创建支付失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_webhook(self, raw_data: bytes, signature: str) -> bool:
        """验证回调签名（模拟版本）"""
        # 模拟环境简化验证
        return True
    
    def query_charge(self, charge_id: str) -> Optional[Dict]:
        """查询支付状态（模拟版本）"""
        try:
            # 模拟查询结果，假设支付总是成功的
            logger.info(f"模拟查询支付状态: {charge_id}")
            
            return {
                'id': charge_id,
                'order_no': charge_id.split('_')[-1] if '_' in charge_id else charge_id,
                'paid': True,  # 模拟环境总是返回已支付
                'status': 'success'
            }
        except Exception as e:
            logger.error(f"查询支付状态失败: {e}")
            return None
    
    def simulate_payment_success(self, order_id: str) -> Dict:
        """模拟支付成功回调"""
        return {
            'type': 'charge.succeeded',
            'data': {
                'object': {
                    'id': f'mock_charge_{int(time.time())}',
                    'order_no': order_id,
                    'paid': True,
                    'amount': 100  # 模拟金额
                }
            }
        }

# 全局实例
reliable_pay_service = ReliablePayService()