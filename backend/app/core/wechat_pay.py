"""
统一的微信支付服务
基于 wechatpy 官方库实现
支持: Native扫码支付、H5支付、JSAPI支付
"""
import os
import logging
import uuid
from typing import Dict, Optional
from decimal import Decimal
from datetime import datetime

from wechatpy.pay import WeChatPay
from wechatpy.pay.utils import calculate_signature
from wechatpy import WeChatClient
from wechatpy.exceptions import WeChatPayException

logger = logging.getLogger(__name__)


class WeChatPayService:
    """微信支付服务 - 统一封装"""

    def __init__(self):
        """初始化微信支付配置（从环境变量读取）"""
        # 从环境变量读取配置
        self.app_id = os.getenv("WECHAT_APP_ID", "")
        self.mch_id = os.getenv("WECHAT_MCH_ID", "")
        self.api_key = os.getenv("WECHAT_API_KEY", "")
        self.notify_url = os.getenv("WECHAT_NOTIFY_URL", "https://tcmlife.top/api/wechat-pay/notify")
        self.h5_domain = os.getenv("WECHAT_H5_DOMAIN", "tcmlife.top")

        # 支付类型配置
        self.payment_type = os.getenv("WECHAT_PAYMENT_TYPE", "NATIVE")  # NATIVE/H5/JSAPI

        # 是否启用模拟模式
        self.mock_mode = os.getenv("WECHAT_MOCK_MODE", "false").lower() == "true"

        # 验证配置完整性
        if not all([self.app_id, self.mch_id, self.api_key]):
            logger.warning("微信支付配置不完整，将启用模拟模式")
            self.mock_mode = True

        # 初始化 wechatpy 客户端
        if not self.mock_mode:
            try:
                self.client = WeChatPay(
                    appid=self.app_id,
                    api_key=self.api_key,
                    mch_id=self.mch_id,
                    sub_mch_id=None,
                    mch_cert=None,
                    mch_key=None
                )
                logger.info(f"✅ 微信支付初始化成功 - AppID: {self.app_id[:8]}***, 商户号: {self.mch_id}")
            except Exception as e:
                logger.error(f"微信支付初始化失败: {e}")
                self.mock_mode = True
                logger.warning("已切换到模拟模式")

    def get_config_info(self) -> Dict:
        """获取配置信息（用于调试）"""
        return {
            "app_id": self.app_id[:8] + "***" if self.app_id else "未配置",
            "mch_id": self.mch_id,
            "payment_type": self.payment_type,
            "notify_url": self.notify_url,
            "h5_domain": self.h5_domain,
            "mock_mode": self.mock_mode
        }

    def create_native_payment(
        self,
        order_id: str,
        amount: Decimal,
        subject: str,
        detail: Optional[str] = None
    ) -> Dict:
        """
        创建Native扫码支付

        Args:
            order_id: 订单号（商户订单号）
            amount: 支付金额（元）
            subject: 商品描述
            detail: 商品详情（可选）

        Returns:
            包含支付二维码URL和支付信息的字典
        """
        if self.mock_mode:
            return self._create_mock_payment(order_id, amount, subject, "NATIVE")

        try:
            # 金额转为分（微信支付单位）
            total_fee = int(amount * 100)

            # 调用统一下单接口
            result = self.client.order.create(
                trade_type='NATIVE',
                body=subject,
                total_fee=total_fee,
                out_trade_no=order_id,
                notify_url=self.notify_url,
                detail=detail,
                product_id=order_id  # 扫码支付必需
            )

            logger.info(f"✅ Native支付创建成功 - 订单号: {order_id}, 金额: ¥{amount}")

            return {
                "success": True,
                "payment_method": "wechat_native",
                "order_id": order_id,
                "amount": float(amount),
                "qr_code_url": result.get("code_url"),  # 二维码链接
                "prepay_id": result.get("prepay_id"),
                "subject": subject,
                "expires_at": datetime.now().timestamp() + 7200  # 2小时有效期
            }

        except WeChatPayException as e:
            logger.error(f"❌ 微信支付创建失败: {e}")
            return {
                "success": False,
                "error": f"微信支付错误: {e.errmsg}",
                "error_code": e.errcode
            }
        except Exception as e:
            logger.error(f"❌ 支付创建异常: {e}")
            return {
                "success": False,
                "error": f"支付服务异常: {str(e)}"
            }

    def create_h5_payment(
        self,
        order_id: str,
        amount: Decimal,
        subject: str,
        client_ip: str = "127.0.0.1",
        detail: Optional[str] = None
    ) -> Dict:
        """
        创建H5支付

        Args:
            order_id: 订单号
            amount: 支付金额（元）
            subject: 商品描述
            client_ip: 用户IP地址
            detail: 商品详情（可选）

        Returns:
            包含支付跳转URL的字典
        """
        if self.mock_mode:
            return self._create_mock_payment(order_id, amount, subject, "H5")

        try:
            total_fee = int(amount * 100)

            # H5支付场景信息
            scene_info = {
                "h5_info": {
                    "type": "Wap",
                    "wap_url": f"https://{self.h5_domain}",
                    "wap_name": "中医健康服务平台"
                }
            }

            result = self.client.order.create(
                trade_type='MWEB',  # H5支付
                body=subject,
                total_fee=total_fee,
                out_trade_no=order_id,
                notify_url=self.notify_url,
                spbill_create_ip=client_ip,
                detail=detail,
                scene_info=scene_info
            )

            logger.info(f"✅ H5支付创建成功 - 订单号: {order_id}, 金额: ¥{amount}")

            return {
                "success": True,
                "payment_method": "wechat_h5",
                "order_id": order_id,
                "amount": float(amount),
                "mweb_url": result.get("mweb_url"),  # H5支付跳转链接
                "prepay_id": result.get("prepay_id"),
                "subject": subject
            }

        except WeChatPayException as e:
            logger.error(f"❌ H5支付创建失败: {e}")
            return {
                "success": False,
                "error": f"微信支付错误: {e.errmsg}",
                "error_code": e.errcode
            }
        except Exception as e:
            logger.error(f"❌ H5支付创建异常: {e}")
            return {
                "success": False,
                "error": f"支付服务异常: {str(e)}"
            }

    def create_jsapi_payment(
        self,
        order_id: str,
        amount: Decimal,
        subject: str,
        openid: str,
        detail: Optional[str] = None
    ) -> Dict:
        """
        创建JSAPI支付（公众号/小程序支付）

        Args:
            order_id: 订单号
            amount: 支付金额（元）
            subject: 商品描述
            openid: 用户的OpenID
            detail: 商品详情（可选）

        Returns:
            包含JSAPI支付参数的字典
        """
        if self.mock_mode:
            return self._create_mock_payment(order_id, amount, subject, "JSAPI", openid=openid)

        try:
            total_fee = int(amount * 100)

            result = self.client.order.create(
                trade_type='JSAPI',
                body=subject,
                total_fee=total_fee,
                out_trade_no=order_id,
                notify_url=self.notify_url,
                openid=openid,  # JSAPI必需
                detail=detail
            )

            # 生成前端JSAPI支付参数
            prepay_id = result.get("prepay_id")
            jsapi_params = self.client.jsapi.get_jsapi_params(prepay_id)

            logger.info(f"✅ JSAPI支付创建成功 - 订单号: {order_id}, OpenID: {openid[:8]}***")

            return {
                "success": True,
                "payment_method": "wechat_jsapi",
                "order_id": order_id,
                "amount": float(amount),
                "prepay_id": prepay_id,
                "jsapi_params": jsapi_params,  # 前端调用微信支付需要的参数
                "subject": subject
            }

        except WeChatPayException as e:
            logger.error(f"❌ JSAPI支付创建失败: {e}")
            return {
                "success": False,
                "error": f"微信支付错误: {e.errmsg}",
                "error_code": e.errcode
            }
        except Exception as e:
            logger.error(f"❌ JSAPI支付创建异常: {e}")
            return {
                "success": False,
                "error": f"支付服务异常: {str(e)}"
            }

    def query_order(self, order_id: str) -> Dict:
        """
        查询订单支付状态

        Args:
            order_id: 商户订单号

        Returns:
            订单状态信息
        """
        if self.mock_mode:
            return {
                "success": True,
                "order_id": order_id,
                "trade_state": "SUCCESS",
                "trade_state_desc": "支付成功（模拟）",
                "mock_mode": True
            }

        try:
            result = self.client.order.query(out_trade_no=order_id)

            return {
                "success": True,
                "order_id": order_id,
                "transaction_id": result.get("transaction_id"),  # 微信支付订单号
                "trade_state": result.get("trade_state"),  # SUCCESS/REFUND/NOTPAY/CLOSED/REVOKED/USERPAYING/PAYERROR
                "trade_state_desc": result.get("trade_state_desc"),
                "total_fee": result.get("total_fee", 0) / 100,  # 转为元
                "paid_at": result.get("time_end"),  # 支付完成时间
                "openid": result.get("openid")
            }

        except WeChatPayException as e:
            logger.error(f"❌ 订单查询失败: {e}")
            return {
                "success": False,
                "error": f"查询失败: {e.errmsg}",
                "error_code": e.errcode
            }
        except Exception as e:
            logger.error(f"❌ 订单查询异常: {e}")
            return {
                "success": False,
                "error": f"查询异常: {str(e)}"
            }

    def verify_notify(self, data: Dict) -> bool:
        """
        验证支付回调签名

        Args:
            data: 微信回调的XML数据（已转为字典）

        Returns:
            签名是否有效
        """
        if self.mock_mode:
            return True

        try:
            signature = data.pop("sign", "")
            calculated_signature = calculate_signature(data, self.api_key)
            return signature == calculated_signature
        except Exception as e:
            logger.error(f"❌ 签名验证失败: {e}")
            return False

    def _create_mock_payment(
        self,
        order_id: str,
        amount: Decimal,
        subject: str,
        payment_type: str,
        openid: Optional[str] = None
    ) -> Dict:
        """创建模拟支付（开发测试用）"""
        logger.info(f"🧪 模拟{payment_type}支付 - 订单: {order_id}, 金额: ¥{amount}")

        mock_prepay_id = f"mock_prepay_{uuid.uuid4().hex[:16]}"

        result = {
            "success": True,
            "payment_method": f"wechat_{payment_type.lower()}",
            "order_id": order_id,
            "amount": float(amount),
            "prepay_id": mock_prepay_id,
            "subject": subject,
            "mock_mode": True
        }

        # 根据支付类型返回不同的模拟数据
        if payment_type == "NATIVE":
            result["qr_code_url"] = f"weixin://wxpay/bizpayurl?pr={mock_prepay_id}"
        elif payment_type == "H5":
            result["mweb_url"] = f"https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?prepay_id={mock_prepay_id}"
        elif payment_type == "JSAPI":
            result["jsapi_params"] = {
                "appId": self.app_id or "mock_app_id",
                "timeStamp": str(int(datetime.now().timestamp())),
                "nonceStr": uuid.uuid4().hex[:16],
                "package": f"prepay_id={mock_prepay_id}",
                "signType": "MD5",
                "paySign": "mock_sign_" + uuid.uuid4().hex[:16]
            }
            result["openid"] = openid or "mock_openid"

        return result


# 全局单例
_wechat_pay_service = None


def get_wechat_pay_service() -> WeChatPayService:
    """获取微信支付服务单例"""
    global _wechat_pay_service
    if _wechat_pay_service is None:
        _wechat_pay_service = WeChatPayService()
    return _wechat_pay_service
