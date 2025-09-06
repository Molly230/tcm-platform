"""
可靠的支付API - 使用Ping++
替代原有的混乱支付代码
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import logging
from datetime import datetime
import json

from app.database import get_db
from app import models
from app.core.reliable_pay import reliable_pay_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/reliable-pay", tags=["可靠支付"])

class PaymentRequest(BaseModel):
    order_id: str
    payment_method: str = "alipay_qr"  # alipay_qr/wechat/alipay

class PaymentResponse(BaseModel):
    success: bool
    payment_url: Optional[str] = None
    charge_id: Optional[str] = None
    message: Optional[str] = None

@router.post("/create", response_model=PaymentResponse)
async def create_reliable_payment(
    request: PaymentRequest, 
    db: Session = Depends(get_db)
):
    """创建可靠的支付订单"""
    try:
        # 查找订单
        order = db.query(models.Order).filter(
            models.Order.order_number == request.order_id
        ).first()
        
        if not order:
            raise HTTPException(status_code=404, detail="订单不存在")
        
        if order.status != models.OrderStatus.PENDING_PAYMENT:
            raise HTTPException(
                status_code=400, 
                detail=f"订单状态不允许支付: {order.status}"
            )
        
        # 创建支付
        result = reliable_pay_service.create_payment(
            order_id=order.order_number,
            amount=order.total_amount,
            subject=f"中医健康平台订单",
            payment_method=request.payment_method
        )
        
        if not result['success']:
            raise HTTPException(
                status_code=500, 
                detail=result.get('error', '支付创建失败')
            )
        
        # 创建支付记录
        payment = models.Payment(
            order_id=order.id,
            payment_method=request.payment_method,
            amount=order.total_amount,
            status="pending",
            transaction_id=result['charge_id']
        )
        db.add(payment)
        db.commit()
        
        logger.info(f"可靠支付创建成功: {order.order_number}")
        
        return PaymentResponse(
            success=True,
            payment_url=result['payment_url'],
            charge_id=result['charge_id'],
            message="支付创建成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建可靠支付失败: {e}")
        raise HTTPException(status_code=500, detail="支付服务异常")

@router.post("/webhook")
async def reliable_payment_webhook(request: Request, db: Session = Depends(get_db)):
    """Ping++支付回调"""
    try:
        # 获取原始数据和签名
        raw_data = await request.body()
        signature = request.headers.get("x-pingplusplus-signature", "")
        
        # 验证签名（生产环境必须开启）
        # if not reliable_pay_service.verify_webhook(raw_data, signature):
        #     logger.warning("支付回调签名验证失败")
        #     return {"message": "signature verification failed"}
        
        # 解析回调数据
        event_data = json.loads(raw_data.decode('utf-8'))
        logger.info(f"收到可靠支付回调: {event_data.get('type')}")
        
        if event_data.get("type") == "charge.succeeded":
            # 支付成功
            charge = event_data.get("data", {}).get("object", {})
            order_number = charge.get("order_no")
            charge_id = charge.get("id")
            
            if not order_number:
                logger.warning("回调缺少订单号")
                return {"message": "missing order_no"}
            
            # 更新订单状态
            order = db.query(models.Order).filter(
                models.Order.order_number == order_number
            ).first()
            
            if not order:
                logger.warning(f"订单不存在: {order_number}")
                return {"message": "order not found"}
            
            # 防重复处理
            if order.status == models.OrderStatus.PAID:
                logger.info(f"订单已支付，跳过: {order_number}")
                return {"message": "already paid"}
            
            # 更新订单和支付记录
            order.status = models.OrderStatus.PAID
            order.paid_at = datetime.utcnow()
            order.payment_id = charge_id
            
            payment = db.query(models.Payment).filter(
                models.Payment.order_id == order.id
            ).first()
            if payment:
                payment.status = "success"
                payment.transaction_id = charge_id
                payment.updated_at = datetime.utcnow()
            
            db.commit()
            logger.info(f"订单支付成功: {order_number}")
        
        return {"message": "success"}
        
    except Exception as e:
        logger.error(f"处理支付回调失败: {e}")
        return {"message": "error"}

@router.get("/status/{order_id}")
async def get_reliable_payment_status(order_id: str, db: Session = Depends(get_db)):
    """查询可靠支付状态"""
    try:
        order = db.query(models.Order).filter(
            models.Order.order_number == order_id
        ).first()
        
        if not order:
            raise HTTPException(status_code=404, detail="订单不存在")
        
        payment = db.query(models.Payment).filter(
            models.Payment.order_id == order.id
        ).first()
        
        # 从支付服务查询最新状态
        charge_status = None
        if payment and payment.transaction_id:
            charge_info = reliable_pay_service.query_charge(payment.transaction_id)
            if charge_info:
                charge_status = charge_info['status']
        
        return {
            "order_id": order_id,
            "order_status": order.status.value,
            "payment_status": payment.status if payment else "none",
            "charge_status": charge_status,
            "amount": float(order.total_amount),
            "paid_at": order.paid_at.isoformat() if order.paid_at else None,
            "mock_mode": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询支付状态失败: {e}")
        raise HTTPException(status_code=500, detail="查询失败")

@router.post("/simulate-success/{order_id}")
async def simulate_payment_success(order_id: str, db: Session = Depends(get_db)):
    """模拟支付成功（仅开发环境使用）"""
    try:
        # 查找订单
        order = db.query(models.Order).filter(
            models.Order.order_number == order_id
        ).first()
        
        if not order:
            raise HTTPException(status_code=404, detail="订单不存在")
        
        # 模拟回调数据
        mock_event = reliable_pay_service.simulate_payment_success(order_id)
        
        # 处理支付成功
        if order.status == models.OrderStatus.PENDING_PAYMENT:
            order.status = models.OrderStatus.PAID
            order.paid_at = datetime.utcnow()
            order.payment_id = mock_event['data']['object']['id']
            
            # 更新支付记录
            payment = db.query(models.Payment).filter(
                models.Payment.order_id == order.id
            ).first()
            if payment:
                payment.status = "success"
                payment.transaction_id = mock_event['data']['object']['id']
                payment.updated_at = datetime.utcnow()
            
            db.commit()
            logger.info(f"模拟支付成功: {order_id}")
            
            return {"message": "支付模拟成功", "order_id": order_id}
        else:
            return {"message": "订单已支付或状态不正确", "order_id": order_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"模拟支付失败: {e}")
        raise HTTPException(status_code=500, detail="模拟支付失败")