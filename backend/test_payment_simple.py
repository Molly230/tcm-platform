#!/usr/bin/env python3
"""
简单的支付API测试 - 不依赖数据库
"""
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import uvicorn

# 创建简单的支付API
app = FastAPI(title="测试支付API")

class PaymentRequest(BaseModel):
    order_id: str
    payment_method: str = "alipay_qr"

class PaymentResponse(BaseModel):
    success: bool
    payment_url: str
    charge_id: str
    message: str

@app.post("/api/reliable-pay/create", response_model=PaymentResponse)
async def create_payment(request: PaymentRequest):
    """创建支付订单"""
    # 模拟支付创建
    charge_id = f"mock_charge_{request.order_id}"
    payment_url = f"https://qr.alipay.com/mock/{charge_id}"
    
    return PaymentResponse(
        success=True,
        payment_url=payment_url,
        charge_id=charge_id,
        message="支付创建成功"
    )

@app.post("/api/reliable-pay/simulate-success/{order_id}")
async def simulate_success(order_id: str):
    """模拟支付成功"""
    return {"message": f"订单 {order_id} 支付成功", "order_id": order_id}

@app.get("/api/reliable-pay/status/{order_id}")
async def get_status(order_id: str):
    """查询支付状态"""
    return {
        "order_id": order_id,
        "order_status": "paid",
        "payment_status": "success",
        "mock_mode": True
    }

@app.get("/api/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}

if __name__ == "__main__":
    print("启动简单支付测试服务器...")
    uvicorn.run(app, host="0.0.0.0", port=8001)