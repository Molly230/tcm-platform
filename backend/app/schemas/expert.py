"""
专家相关的Pydantic模型
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ExpertCategory(str, Enum):
    INTERNAL = "internal"  # 中医内科
    GYNECOLOGY = "gynecology"  # 中医妇科
    PEDIATRICS = "pediatrics"  # 中医儿科
    ACUPUNCTURE = "acupuncture"  # 针灸推拿
    HEALTH = "health"  # 中医养生

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