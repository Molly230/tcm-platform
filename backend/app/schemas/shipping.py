"""
配送相关的Pydantic Schema
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class TrackingHistoryItem(BaseModel):
    """物流轨迹项"""
    time: str
    status: str
    location: Optional[str] = None


class ShippingCreate(BaseModel):
    """创建配送记录请求"""
    order_id: int = Field(..., description="订单ID")
    courier_company: str = Field(..., description="物流公司代码")
    courier_company_name: Optional[str] = Field(None, description="物流公司名称")
    tracking_number: str = Field(..., description="物流单号")
    courier_name: Optional[str] = Field(None, description="配送员姓名")
    courier_phone: Optional[str] = Field(None, description="配送员电话")
    notes: Optional[str] = Field(None, description="备注")


class ShippingUpdate(BaseModel):
    """更新配送记录请求"""
    courier_company: Optional[str] = None
    courier_company_name: Optional[str] = None
    tracking_number: Optional[str] = None
    courier_name: Optional[str] = None
    courier_phone: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class ShippingResponse(BaseModel):
    """配送记录响应"""
    id: int
    order_id: int
    courier_company: str
    courier_company_name: Optional[str]
    tracking_number: str
    status: str
    courier_name: Optional[str]
    courier_phone: Optional[str]
    shipped_at: Optional[datetime]
    estimated_delivery_at: Optional[datetime]
    delivered_at: Optional[datetime]
    tracking_history: List[TrackingHistoryItem] = []
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrackingQueryRequest(BaseModel):
    """物流查询请求"""
    order_id: int = Field(..., description="订单ID")


class TrackingQueryResponse(BaseModel):
    """物流查询响应"""
    success: bool
    courier_code: Optional[str]
    tracking_number: Optional[str]
    shipping_status: Optional[str]
    tracking_history: List[TrackingHistoryItem] = []
    last_update: Optional[str]
    error: Optional[str] = None
