"""
课程相关API路由
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

router = APIRouter(tags=["courses"])

@router.post("/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    """创建新课程"""
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/", response_model=List[schemas.Course])
def read_courses(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    """获取课程列表"""
    query = db.query(models.Course)
    if category:
        query = query.filter(models.Course.category == category)
    courses = query.offset(skip).limit(limit).all()
    return courses

@router.get("/{course_id}", response_model=schemas.Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    """获取特定课程"""
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise CommonErrors.COURSE_NOT_FOUND
    return db_course

@router.put("/{course_id}", response_model=schemas.Course)
def update_course(
    course_id: int,
    course_update: schemas.CourseUpdate,
    db: Session = Depends(get_db)
):
    """更新课程信息"""
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise CommonErrors.COURSE_NOT_FOUND
    
    # 更新课程信息
    for field, value in course_update.dict(exclude_unset=True).items():
        setattr(db_course, field, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/{course_id}/lessons", response_model=List[schemas.Lesson])
def get_course_lessons(course_id: int, db: Session = Depends(get_db)):
    """获取课程的所有课时"""
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise CommonErrors.COURSE_NOT_FOUND
    
    lessons = db.query(models.Lesson).filter(
        models.Lesson.course_id == course_id
    ).order_by(models.Lesson.order).all()
    
    return lessons

@router.post("/{course_id}/enroll")
def enroll_course(
    course_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """用户报名课程"""
    # 检查课程是否存在
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise CommonErrors.COURSE_NOT_FOUND
    
    # 检查是否已经报名
    existing_enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.user_id == user_id,
        models.Enrollment.course_id == course_id
    ).first()
    
    if existing_enrollment:
        raise BusinessException("已经报名该课程")
    
    # 创建报名记录
    enrollment = models.Enrollment(
        user_id=user_id,
        course_id=course_id
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    return {"message": "报名成功", "enrollment_id": enrollment.id}

@router.get("/{course_id}/enrollment/{user_id}")
def get_user_enrollment(
    course_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取用户的课程报名信息"""
    enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.user_id == user_id,
        models.Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        return {"enrolled": False}
    
    return {
        "enrolled": True,
        "progress": enrollment.progress,
        "completed_lessons": enrollment.completed_lessons,
        "total_watch_time": enrollment.total_watch_time,
        "last_watched_lesson_id": enrollment.last_watched_lesson_id
    }

@router.delete("/{course_id}", response_model=schemas.Course)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """删除课程"""
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise CommonErrors.COURSE_NOT_FOUND
    
    db.delete(db_course)
    db.commit()
    return db_course

@router.get("/lessons/{lesson_id}", response_model=schemas.Lesson)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """获取单个课时详情"""
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise NotFoundException("课时")
    return lesson

@router.post("/lessons/{lesson_id}/complete")
def mark_lesson_complete(
    lesson_id: int,
    user_data: dict,
    db: Session = Depends(get_db)
):
    """标记课时完成"""
    user_id = user_data.get('user_id', 'anonymous')
    
    # 这里可以添加实际的完成记录逻辑
    # 比如更新用户的学习进度等
    
    return {"message": "课时标记完成", "lesson_id": lesson_id, "user_id": user_id}