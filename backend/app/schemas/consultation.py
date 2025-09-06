"""
健康咨询相关的Pydantic模型
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ConsultationType(str, Enum):
    AI = "ai"
    TEXT = "text"
    VOICE = "voice"
    VIDEO = "video"

class ConsultationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ConsultationBase(BaseModel):
    user_id: int
    expert_id: Optional[int] = None
    type: ConsultationType
    symptoms: Optional[str] = None
    duration: Optional[str] = None
    medical_history: Optional[str] = None
    ai_response: Optional[str] = None
    expert_notes: Optional[str] = None
    rating: Optional[float] = None
    price: Optional[float] = None

class ConsultationCreate(ConsultationBase):
    pass

class ConsultationUpdate(BaseModel):
    status: Optional[ConsultationStatus] = None
    ai_response: Optional[str] = None
    expert_notes: Optional[str] = None
    rating: Optional[float] = None

class Consultation(ConsultationBase):
    id: int
    status: ConsultationStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True