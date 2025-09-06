"""
Stripe支付服务 - 国际标准，最可靠
支持支付宝、微信支付、信用卡等
"""
import stripe
import logging
from typing import Dict, Optional
from decimal import Decimal
import os

logger = logging.getLogger(__name__)

class StripePayService:
    """基于Stripe的支付服务"""
    
    def __init__(self):
        # Stripe配置（测试环境）
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_...')
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_...')
        
    def create_payment(self, order_id: str, amount: Decimal, 
                      description: str = "中医健康平台订单") -> Dict:
        """
        创建Stripe支付
        
        Args:
            order_id: 订单号
            amount: 金额（元）
            description: 商品描述
        
        Returns:
            包含client_secret的支付信息
        """
        try:
            # 金额转换为分
            amount_cents = int(amount * 100)
            
            # 创建PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='cny',
                description=description,
                metadata={'order_id': order_id},
                # 支持的支付方式
                payment_method_types=[
                    'card',           # 信用卡
                    'alipay',         # 支付宝
                    'wechat_pay'      # 微信支付
                ]
            )
            
            logger.info(f"Stripe支付创建成功: {order_id}, intent_id: {intent.id}")
            
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'publishable_key': os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_...')
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe支付创建失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_webhook(self, payload: bytes, sig_header: str) -> Optional[Dict]:
        """验证Stripe Webhook"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            return event
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            logger.error(f"Webhook验证失败: {e}")
            return None
    
    def get_payment_status(self, payment_intent_id: str) -> Dict:
        """获取支付状态"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                'status': intent.status,
                'paid': intent.status == 'succeeded',
                'order_id': intent.metadata.get('order_id'),
                'amount': intent.amount / 100  # 转回元
            }
        except stripe.error.StripeError as e:
            logger.error(f"查询支付状态失败: {e}")
            return {'status': 'error', 'error': str(e)}

# 全局实例
stripe_pay_service = StripePayService()