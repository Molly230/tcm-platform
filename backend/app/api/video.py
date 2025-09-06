"""
视频播放、上传和管理相关API
"""
import time
import os
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app import schemas, models
from app.schemas.course import VideoStatus
from app.database import get_db
from app.core.video_security import video_security_service, video_watermark_service
from app.core.permissions import get_current_user, require_admin_role
from app.core.config import settings

router = APIRouter(tags=["video"])

@router.get("/lessons/{lesson_id}/play-url")
def get_video_play_url(
    lesson_id: int,
    user_id: str = Query(..., description="用户ID"),
    db: Session = Depends(get_db)
):
    """获取安全的视频播放URL"""
    
    # 获取课程信息
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在"
        )
    
    # 检查课程是否可用
    if lesson.status != models.VideoStatus.READY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="视频正在处理中，请稍后再试"
        )
    
    # 检查用户是否有权限观看（这里需要根据实际业务逻辑实现）
    course = lesson.course
    
    # 如果课程是免费的或课时是免费的，允许直接观看
    if not course.is_free and not lesson.is_free and not course.is_published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="课程未发布"
        )
    
    # 如果不是免费课程，需要检查用户是否已购买
    if not lesson.is_free and not course.is_free:
        enrollment = db.query(models.Enrollment).filter(
            models.Enrollment.user_id == int(user_id),
            models.Enrollment.course_id == course.id
        ).first()
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="请先购买课程"
            )
    
    # 生成用户水印
    watermark_text = video_watermark_service.generate_user_watermark(
        user_id, f"用户{user_id}"
    )
    
    # 生成安全的播放URL
    secure_url = video_security_service.generate_secure_url(
        video_id=lesson.video_id or lesson.file_id,
        user_id=user_id,
        expire_time=7200,  # 2小时有效期
        watermark=watermark_text
    )
    
    # 生成访问token
    access_token = video_security_service.generate_token_for_lesson(
        lesson_id=lesson_id,
        user_id=user_id,
        course_id=course.id
    )
    
    return {
        "video_url": secure_url,
        "access_token": access_token,
        "watermark_config": video_watermark_service.get_watermark_config(user_id, f"用户{user_id}"),
        "lesson_info": {
            "id": lesson.id,
            "title": lesson.title,
            "duration": lesson.duration,
            "course_title": course.title
        },
        "security_config": {
            "disable_right_click": True,
            "disable_dev_tools": True,
            "disable_screen_capture": True,
            "heartbeat_interval": 30  # 心跳检测间隔（秒）
        }
    }

@router.post("/lessons/{lesson_id}/heartbeat")
def video_heartbeat(
    lesson_id: int,
    user_id: str,
    current_time: int,
    token: str,
    db: Session = Depends(get_db)
):
    """视频播放心跳检测"""
    
    # 验证token
    token_data = video_security_service.verify_lesson_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的访问token"
        )
    
    if token_data['lesson_id'] != lesson_id or token_data['user_id'] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="token不匹配"
        )
    
    # 更新观看记录
    watch_record = db.query(models.WatchRecord).filter(
        models.WatchRecord.lesson_id == lesson_id,
        models.WatchRecord.user_id == int(user_id)
    ).first()
    
    if not watch_record:
        watch_record = models.WatchRecord(
            lesson_id=lesson_id,
            user_id=int(user_id),
            watch_time=current_time,
            last_position=current_time
        )
        db.add(watch_record)
    else:
        watch_record.watch_time = max(watch_record.watch_time, current_time)
        watch_record.last_position = current_time
        
        # 检查是否观看完成（观看超过90%算完成）
        lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
        if lesson and lesson.duration:
            completion_threshold = lesson.duration * 0.9
            if current_time >= completion_threshold:
                watch_record.is_completed = True
    
    db.commit()
    
    return {
        "status": "success", 
        "server_time": int(time.time()),
        "continue_play": True
    }

@router.get("/lessons/{lesson_id}/progress")
def get_video_progress(
    lesson_id: int,
    user_id: str = Query(..., description="用户ID"),
    db: Session = Depends(get_db)
):
    """获取用户观看进度"""
    
    watch_record = db.query(models.WatchRecord).filter(
        models.WatchRecord.lesson_id == lesson_id,
        models.WatchRecord.user_id == int(user_id)
    ).first()
    
    if not watch_record:
        return {
            "lesson_id": lesson_id,
            "last_position": 0,
            "watch_time": 0,
            "is_completed": False
        }
    
    return {
        "lesson_id": lesson_id,
        "last_position": watch_record.last_position,
        "watch_time": watch_record.watch_time,
        "is_completed": watch_record.is_completed
    }

# =============================================================================
# 管理员视频管理功能
# =============================================================================

@router.get("/admin/lessons", response_model=List[schemas.Lesson])
def get_admin_lessons(
    skip: int = 0,
    limit: int = 100,
    course_id: Optional[int] = Query(None, description="课程ID筛选"),
    status: Optional[VideoStatus] = Query(None, description="视频状态筛选"),
    current_user: models.User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """管理员获取所有课程列表"""
    query = db.query(models.Lesson)
    
    if course_id:
        query = query.filter(models.Lesson.course_id == course_id)
    
    if status:
        query = query.filter(models.Lesson.status == status)
    
    lessons = query.offset(skip).limit(limit).all()
    return lessons

@router.post("/admin/lessons", response_model=schemas.Lesson)
def create_lesson(
    lesson_data: schemas.LessonCreate,
    current_user: models.User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """管理员创建新课程"""
    
    # 检查课程是否存在
    course = db.query(models.Course).filter(models.Course.id == lesson_data.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在"
        )
    
    # 创建新课程
    db_lesson = models.Lesson(**lesson_data.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    
    # 更新课程的总课程数
    course.total_lessons = db.query(models.Lesson).filter(models.Lesson.course_id == course.id).count()
    if lesson_data.duration:
        course.total_duration = db.query(models.Lesson).filter(
            models.Lesson.course_id == course.id
        ).with_entities(models.Lesson.duration).all()
        course.total_duration = sum([l[0] or 0 for l in course.total_duration])
    
    db.commit()
    
    return db_lesson

@router.put("/admin/lessons/{lesson_id}", response_model=schemas.Lesson)
def update_lesson(
    lesson_id: int,
    lesson_data: schemas.LessonUpdate,
    current_user: models.User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """管理员更新课程信息"""
    
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在"
        )
    
    # 更新课程信息
    for field, value in lesson_data.dict(exclude_unset=True).items():
        if hasattr(lesson, field):
            setattr(lesson, field, value)
    
    lesson.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(lesson)
    
    return lesson

@router.delete("/admin/lessons/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    current_user: models.User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """管理员删除课程"""
    
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在"
        )
    
    # 删除课程（软删除 - 在实际项目中可能需要保留数据）
    course_id = lesson.course_id
    db.delete(lesson)
    db.commit()
    
    # 更新课程统计信息
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course:
        course.total_lessons = db.query(models.Lesson).filter(models.Lesson.course_id == course_id).count()
        remaining_lessons = db.query(models.Lesson).filter(models.Lesson.course_id == course_id).all()
        course.total_duration = sum([l.duration or 0 for l in remaining_lessons])
        db.commit()
    
    return {"message": "课程删除成功"}

@router.post("/admin/lessons/upload")
async def upload_video(
    file: UploadFile = File(...),
    course_id: int = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    order: int = Form(...),
    is_free: bool = Form(False),
    current_user: models.User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """管理员上传视频文件"""
    
    # 检查课程是否存在
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在"
        )
    
    # 检查文件类型
    allowed_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的视频格式。支持的格式: mp4, avi, mov, wmv, flv, webm"
        )
    
    # 检查文件大小 (最大500MB)
    max_size = 500 * 1024 * 1024  # 500MB
    if file.size and file.size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="视频文件过大，最大支持500MB"
        )
    
    try:
        # 创建上传目录
        upload_dir = "uploads/videos"
        os.makedirs(upload_dir, exist_ok=True)
        
        # 生成唯一文件名
        timestamp = int(time.time())
        filename = f"{timestamp}_{course_id}_{order}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 创建课程记录
        lesson_data = {
            "course_id": course_id,
            "title": title,
            "description": description,
            "order": order,
            "is_free": is_free,
            "video_url": f"/uploads/videos/{filename}",
            "file_id": filename,  # 使用文件名作为file_id
            "status": models.VideoStatus.READY,  # 本地文件直接标记为就绪
        }
        
        db_lesson = models.Lesson(**lesson_data)
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        
        # 更新课程统计
        course.total_lessons = db.query(models.Lesson).filter(models.Lesson.course_id == course_id).count()
        db.commit()
        
        return {
            "message": "视频上传成功",
            "lesson": db_lesson,
            "file_info": {
                "filename": filename,
                "size": len(content),
                "path": file_path
            }
        }
        
    except Exception as e:
        # 如果出错，尝试清理已上传的文件
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"视频上传失败: {str(e)}"
        )

@router.get("/admin/lessons/{lesson_id}/info", response_model=schemas.Lesson)
def get_lesson_info(
    lesson_id: int,
    current_user: models.User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """获取课程详细信息（管理员）"""
    
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在"
        )
    
    return lesson

@router.post("/admin/lessons/{lesson_id}/process")
def process_video(
    lesson_id: int,
    current_user: models.User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """处理视频（转码、生成封面等）"""
    
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在"
        )
    
    # 这里应该启动视频处理任务（异步）
    # 在实际项目中可能会调用腾讯云、阿里云等服务
    # 目前模拟处理过程
    
    lesson.status = models.VideoStatus.PROCESSING
    db.commit()
    
    # TODO: 实际的视频处理逻辑
    # - 视频转码
    # - 生成封面图
    # - 提取视频信息（时长、分辨率等）
    # - 上传到CDN
    
    return {
        "message": "视频处理任务已启动",
        "lesson_id": lesson_id,
        "status": "processing"
    }