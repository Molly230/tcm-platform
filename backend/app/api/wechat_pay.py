"""
微信支付API路由
支持 Native扫码支付、H5支付、JSAPI支付
"""
from fastapi import APIRouter, Depends, HTTPException, Request, Body
from fastapi.responses import HTMLResponse, PlainTextResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, Literal
from decimal import Decimal
import logging
import xml.etree.ElementTree as ET

from app.database import get_db
from app import models
from app.core.wechat_pay import get_wechat_pay_service
from app.core.permissions import get_current_user
from app.core.enums_v2 import OrderStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/wechat-pay", tags=["微信支付"])


# ==================== Pydantic 模型定义 ====================

class NativePaymentRequest(BaseModel):
    """Native扫码支付请求"""
    order_id: int = Field(..., description="订单ID")
    detail: Optional[str] = Field(None, description="商品详情")


class H5PaymentRequest(BaseModel):
    """H5支付请求"""
    order_id: int = Field(..., description="订单ID")
    detail: Optional[str] = Field(None, description="商品详情")


class JSAPIPaymentRequest(BaseModel):
    """JSAPI支付请求"""
    order_id: int = Field(..., description="订单ID")
    openid: str = Field(..., description="用户OpenID")
    detail: Optional[str] = Field(None, description="商品详情")


class QueryPaymentRequest(BaseModel):
    """查询支付状态请求"""
    order_number: str = Field(..., description="商户订单号")


# ==================== API 端点 ====================

@router.get("/config")
def get_payment_config():
    """
    获取微信支付配置信息（调试用）
    """
    service = get_wechat_pay_service()
    return {
        "service_name": "微信支付",
        "version": "v1.0",
        "supported_types": ["NATIVE", "H5", "JSAPI"],
        "config": service.get_config_info()
    }


@router.post("/native")
def create_native_payment(
    request: NativePaymentRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    创建Native扫码支付

    返回二维码URL，前端可以用qrcode库生成二维码图片
    """
    # 查询订单
    order = db.query(models.Order).filter(
        models.Order.id == request.order_id,
        models.Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"订单状态不允许支付: {order.status}")

    # 创建支付
    service = get_wechat_pay_service()
    result = service.create_native_payment(
        order_id=order.order_number,
        amount=order.total_amount,
        subject=f"订单 {order.order_number}",
        detail=request.detail
    )

    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "支付创建失败"))

    logger.info(f"✅ Native支付创建 - 用户: {current_user.username}, 订单: {order.order_number}")

    return {
        "success": True,
        "message": "支付创建成功",
        "data": result
    }


@router.post("/h5")
def create_h5_payment(
    request: H5PaymentRequest,
    client_request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    创建H5支付

    返回支付跳转链接，前端直接跳转即可
    """
    # 查询订单
    order = db.query(models.Order).filter(
        models.Order.id == request.order_id,
        models.Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"订单状态不允许支付: {order.status}")

    # 获取客户端IP
    client_ip = client_request.client.host if client_request.client else "127.0.0.1"

    # 创建支付
    service = get_wechat_pay_service()
    result = service.create_h5_payment(
        order_id=order.order_number,
        amount=order.total_amount,
        subject=f"订单 {order.order_number}",
        client_ip=client_ip,
        detail=request.detail
    )

    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "支付创建失败"))

    logger.info(f"✅ H5支付创建 - 用户: {current_user.username}, 订单: {order.order_number}")

    return {
        "success": True,
        "message": "支付创建成功",
        "data": result
    }


@router.post("/jsapi")
def create_jsapi_payment(
    request: JSAPIPaymentRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    创建JSAPI支付（公众号/小程序）

    返回前端调用微信支付所需的参数
    """
    # 查询订单
    order = db.query(models.Order).filter(
        models.Order.id == request.order_id,
        models.Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"订单状态不允许支付: {order.status}")

    # 创建支付
    service = get_wechat_pay_service()
    result = service.create_jsapi_payment(
        order_id=order.order_number,
        amount=order.total_amount,
        subject=f"订单 {order.order_number}",
        openid=request.openid,
        detail=request.detail
    )

    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "支付创建失败"))

    logger.info(f"✅ JSAPI支付创建 - 用户: {current_user.username}, 订单: {order.order_number}")

    return {
        "success": True,
        "message": "支付创建成功",
        "data": result
    }


@router.post("/query")
def query_payment_status(
    request: QueryPaymentRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    查询支付状态
    """
    try:
        # 验证订单归属
        order = db.query(models.Order).filter(
            models.Order.order_number == request.order_number,
            models.Order.user_id == current_user.id
        ).first()

        if not order:
            raise HTTPException(status_code=404, detail="订单不存在")

        # 查询支付状态
        service = get_wechat_pay_service()
        result = service.query_order(order_id=request.order_number)

        if not result.get("success"):
            logger.warning(f"支付查询失败: {result.get('error')}")
            # 返回订单当前状态而不是直接报错
            return {
                "success": True,
                "message": "查询成功(从订单状态)",
                "data": {
                    "trade_state": "NOTPAY" if order.status == OrderStatus.PENDING else "SUCCESS",
                    "order_number": order.order_number,
                    "mock_mode": service.mock_mode
                }
            }

        # 如果支付成功，更新订单状态
        if result.get("trade_state") == "SUCCESS" and order.status == OrderStatus.PENDING:
            order.status = OrderStatus.PAID
            order.paid_at = result.get("paid_at")
            db.commit()
            logger.info(f"✅ 订单支付成功 - 订单号: {order.order_number}")

        return {
            "success": True,
            "message": "查询成功",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询支付状态异常: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"查询支付状态失败: {str(e)}")


@router.post("/notify", response_class=PlainTextResponse)
async def payment_notify(request: Request, db: Session = Depends(get_db)):
    """
    微信支付回调通知

    微信服务器会POST XML格式的支付结果
    """
    try:
        # 读取XML数据
        body = await request.body()
        xml_data = body.decode("utf-8")

        # 解析XML
        root = ET.fromstring(xml_data)
        data = {child.tag: child.text for child in root}

        logger.info(f"收到微信支付回调: {data.get('out_trade_no')}")

        # 验证签名
        service = get_wechat_pay_service()
        if not service.verify_notify(data.copy()):
            logger.error("❌ 微信支付回调签名验证失败")
            return _generate_notify_response(False, "签名验证失败")

        # 验证返回码
        return_code = data.get("return_code")
        result_code = data.get("result_code")

        if return_code != "SUCCESS" or result_code != "SUCCESS":
            logger.error(f"❌ 微信支付失败: {data.get('err_code_des')}")
            return _generate_notify_response(True, "OK")

        # 查询订单
        order_number = data.get("out_trade_no")
        order = db.query(models.Order).filter(
            models.Order.order_number == order_number
        ).first()

        if not order:
            logger.error(f"❌ 订单不存在: {order_number}")
            return _generate_notify_response(False, "订单不存在")

        # 更新订单状态
        if order.status == OrderStatus.PENDING:
            order.status = OrderStatus.PAID
            order.transaction_id = data.get("transaction_id")  # 微信支付订单号
            order.paid_at = data.get("time_end")
            db.commit()
            logger.info(f"✅ 订单支付成功（回调） - 订单号: {order_number}")

        # 返回成功响应
        return _generate_notify_response(True, "OK")

    except Exception as e:
        logger.error(f"❌ 处理微信支付回调异常: {e}")
        return _generate_notify_response(False, f"处理失败: {str(e)}")


def _generate_notify_response(success: bool, message: str) -> str:
    """生成微信支付回调响应XML"""
    return_code = "SUCCESS" if success else "FAIL"
    return f"""<xml>
  <return_code><![CDATA[{return_code}]]></return_code>
  <return_msg><![CDATA[{message}]]></return_msg>
</xml>"""


@router.get("/mock/simulate-success/{order_number}")
def simulate_payment_success(
    order_number: str,
    db: Session = Depends(get_db)
):
    """
    模拟支付成功（仅用于开发测试）
    """
    service = get_wechat_pay_service()

    if not service.mock_mode:
        raise HTTPException(status_code=403, detail="此接口仅在模拟模式下可用")

    # 查询订单
    order = db.query(models.Order).filter(
        models.Order.order_number == order_number
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    # 更新订单状态
    if order.status == models.OrderStatus.PENDING:
        order.status = OrderStatus.PAID
        order.transaction_id = f"MOCK_{order_number}"
        from datetime import datetime
        order.paid_at = datetime.now()
        db.commit()

    logger.info(f"🧪 模拟支付成功 - 订单号: {order_number}")

    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>支付成功</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0fff0; }}
            .success {{ color: #07c160; font-size: 48px; margin: 20px 0; }}
            .info {{ color: #666; font-size: 18px; margin: 10px 0; }}
            button {{ padding: 15px 40px; background: #07c160; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; margin-top: 30px; }}
            button:hover {{ background: #06ad56; }}
        </style>
    </head>
    <body>
        <div class="success">✅</div>
        <h1 style="color: #07c160;">支付成功！</h1>
        <p class="info">订单号: {order_number}</p>
        <p class="info">支付方式: 微信支付（模拟）</p>
        <button onclick="window.close()">关闭页面</button>
        <script>
            // 5秒后自动关闭
            setTimeout(() => window.close(), 5000);
        </script>
    </body>
    </html>
    """)
