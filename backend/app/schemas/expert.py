"""
专家相关的Pydantic模型
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.core.enums_v2 import ExpertCategory

class ExpertBase(BaseModel):
    name: str
    title: Optional[str] = None
    category: ExpertCategory
    avatar_url: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    consultation_count: int = 0
    text_price: Optional[float] = None
    voice_price: Optional[float] = None
    video_price: Optional[float] = None
    is_active: bool = True

class ExpertCreate(ExpertBase):
    pass

class ExpertUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    category: Optional[ExpertCategory] = None
    avatar_url: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    consultation_count: Optional[int] = None
    text_price: Optional[float] = None
    voice_price: Optional[float] = None
    video_price: Optional[float] = None
    is_active: Optional[bool] = None

class Expert(ExpertBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True