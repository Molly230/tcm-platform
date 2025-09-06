"""
健康咨询相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models
from app.database import get_db

router = APIRouter(tags=["consultations"])

@router.post("/", response_model=schemas.Consultation)
def create_consultation(
    consultation: schemas.ConsultationCreate,
    db: Session = Depends(get_db)
):
    """创建健康咨询记录"""
    db_consultation = models.Consultation(**consultation.dict())
    db.add(db_consultation)
    db.commit()
    db.refresh(db_consultation)
    return db_consultation

@router.get("/", response_model=List[schemas.Consultation])
def read_consultations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取健康咨询记录列表"""
    consultations = db.query(models.Consultation).offset(skip).limit(limit).all()
    return consultations

@router.get("/{consultation_id}", response_model=schemas.Consultation)
def read_consultation(consultation_id: int, db: Session = Depends(get_db)):
    """获取特定健康咨询记录"""
    db_consultation = db.query(models.Consultation).filter(
        models.Consultation.id == consultation_id
    ).first()
    if db_consultation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    return db_consultation

@router.put("/{consultation_id}", response_model=schemas.Consultation)
def update_consultation(
    consultation_id: int,
    consultation_update: schemas.ConsultationUpdate,
    db: Session = Depends(get_db)
):
    """更新健康咨询记录"""
    db_consultation = db.query(models.Consultation).filter(
        models.Consultation.id == consultation_id
    ).first()
    if db_consultation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # 更新咨询记录
    for field, value in consultation_update.dict(exclude_unset=True).items():
        setattr(db_consultation, field, value)
    
    db.commit()
    db.refresh(db_consultation)
    return db_consultation

@router.delete("/{consultation_id}", response_model=schemas.Consultation)
def delete_consultation(consultation_id: int, db: Session = Depends(get_db)):
    """删除健康咨询记录"""
    db_consultation = db.query(models.Consultation).filter(
        models.Consultation.id == consultation_id
    ).first()
    if db_consultation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    db.delete(db_consultation)
    db.commit()
    return db_consultation