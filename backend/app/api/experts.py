"""
专家相关API路由
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models
from app.database import get_db
from app.core.exceptions import (
    NotFoundException, 
    BusinessException, 
    ValidationException, 
    FileTooLargeException, 
    UnsupportedFileTypeException, 
    DatabaseException, 
    CommonErrors
)

router = APIRouter(tags=["experts"])

@router.post("/", response_model=schemas.Expert)
def create_expert(expert: schemas.ExpertCreate, db: Session = Depends(get_db)):
    """创建新专家"""
    db_expert = models.Expert(**expert.dict())
    db.add(db_expert)
    db.commit()
    db.refresh(db_expert)
    return db_expert

@router.get("/", response_model=List[schemas.Expert])
def read_experts(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    """获取专家列表"""
    query = db.query(models.Expert)
    if category:
        query = query.filter(models.Expert.category == category)
    experts = query.offset(skip).limit(limit).all()
    return experts

@router.get("/{expert_id}", response_model=schemas.Expert)
def read_expert(expert_id: int, db: Session = Depends(get_db)):
    """获取特定专家"""
    db_expert = db.query(models.Expert).filter(models.Expert.id == expert_id).first()
    if db_expert is None:
        raise CommonErrors.EXPERT_NOT_FOUND
    return db_expert

@router.put("/{expert_id}", response_model=schemas.Expert)
def update_expert(
    expert_id: int,
    expert_update: schemas.ExpertUpdate,
    db: Session = Depends(get_db)
):
    """更新专家信息"""
    db_expert = db.query(models.Expert).filter(models.Expert.id == expert_id).first()
    if db_expert is None:
        raise CommonErrors.EXPERT_NOT_FOUND
    
    # 更新专家信息
    for field, value in expert_update.dict(exclude_unset=True).items():
        setattr(db_expert, field, value)
    
    db.commit()
    db.refresh(db_expert)
    return db_expert

@router.delete("/{expert_id}", response_model=schemas.Expert)
def delete_expert(expert_id: int, db: Session = Depends(get_db)):
    """删除专家"""
    db_expert = db.query(models.Expert).filter(models.Expert.id == expert_id).first()
    if db_expert is None:
        raise CommonErrors.EXPERT_NOT_FOUND
    
    db.delete(db_expert)
    db.commit()
    return db_expert