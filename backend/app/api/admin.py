"""
管理后台API
"""
import os
import uuid
import csv
import io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from app.core.exceptions import (
    NotFoundException, BusinessException, ValidationException,
    FileTooLargeException, UnsupportedFileTypeException, DatabaseException,
    CommonErrors
)
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app import schemas, models
from app.database import get_db
from app.core.permissions import require_admin_role, get_current_user
from app.core.logger import log_admin_action, log_file_upload, log_data_export, admin_logger
from app.core.enums_v2 import AuditStatus, ExpertStatus, ProductStatus, OrderStatus, ConsultationStatus, ConsultationType

router = APIRouter(tags=["admin"])

# ====== 课程管理 ======

@router.post("/test")
def test_create():
    """测试API端点"""
    from app.core.response import ApiResponse
    admin_logger.logger.info("测试API被调用")
    return ApiResponse.success(message="管理员API测试成功")

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db), current_user: models.User = Depends(require_admin_role)):
    """获取管理后台统计数据"""
    from app.core.response import ApiResponse
    
    try:
        # 基础统计
        total_users = db.query(models.User).count()
        total_experts = db.query(models.Expert).count()
        total_courses = db.query(models.Course).count()
        total_products = db.query(models.Product).count()
        
        stats = {
            "overview": {
                "total_users": total_users,
                "total_experts": total_experts, 
                "total_courses": total_courses,
                "total_products": total_products
            },
            "today": {
                "new_users": 0,  # 可以后续添加具体逻辑
                "new_orders": 0,
                "revenue": 0.0
            }
        }
        
        return ApiResponse.success(stats, "统计数据获取成功")
    except Exception as e:
        return ApiResponse.error(f"获取统计数据失败: {str(e)}", 500)

@router.get("/courses", response_model=List[schemas.Course])
def get_all_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取所有课程（包括未发布的）"""
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    return courses

@router.post("/courses", response_model=schemas.Course)
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """创建新课程"""
    admin_logger.logger.info(f"接收到课程创建请求: {course.dict()}")
    admin_logger.logger.info(f"当前用户: {current_user.email}")
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    
    # 记录操作日志
    log_admin_action(
        current_user, 
        "创建课程", 
        f"课程ID:{db_course.id}", 
        f"课程标题:{db_course.title}"
    )
    
    return db_course

@router.put("/courses/{course_id}", response_model=schemas.Course)
def update_course(
    course_id: int,
    course_update: schemas.CourseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """更新课程信息"""
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise CommonErrors.COURSE_NOT_FOUND
    
    for field, value in course_update.dict(exclude_unset=True).items():
        setattr(db_course, field, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """删除课程"""
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise CommonErrors.COURSE_NOT_FOUND
    
    course_title = db_course.title  # 保存标题用于日志
    db.delete(db_course)
    db.commit()
    
    # 记录操作日志
    log_admin_action(
        current_user, 
        "删除课程", 
        f"课程ID:{course_id}", 
        f"课程标题:{course_title}"
    )
    
    return {"message": "Course deleted successfully"}

# ====== 课时管理 ======

@router.get("/courses/{course_id}/lessons", response_model=List[schemas.Lesson])
def get_course_lessons(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取课程的所有课时"""
    lessons = db.query(models.Lesson).filter(
        models.Lesson.course_id == course_id
    ).order_by(models.Lesson.order).all()
    return lessons

@router.post("/courses/{course_id}/lessons", response_model=schemas.Lesson)
def create_lesson(
    course_id: int,
    lesson: schemas.LessonCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """创建新课时"""
    # 检查课程是否存在
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise CommonErrors.COURSE_NOT_FOUND
    
    # 如果没有指定顺序，自动设置为最后一个
    if not lesson.order:
        max_order = db.query(models.Lesson).filter(
            models.Lesson.course_id == course_id
        ).count()
        lesson.order = max_order + 1
    
    lesson_data = lesson.dict()
    lesson_data['course_id'] = course_id
    
    db_lesson = models.Lesson(**lesson_data)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    
    # 更新课程的总课时数
    course.total_lessons = db.query(models.Lesson).filter(
        models.Lesson.course_id == course_id
    ).count()
    db.commit()
    
    return db_lesson

@router.put("/lessons/{lesson_id}", response_model=schemas.Lesson)
def update_lesson(
    lesson_id: int,
    lesson_update: schemas.LessonUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """更新课时信息"""
    db_lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not db_lesson:
        raise NotFoundException("课时")
    
    for field, value in lesson_update.dict(exclude_unset=True).items():
        setattr(db_lesson, field, value)
    
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@router.delete("/lessons/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """删除课时"""
    db_lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not db_lesson:
        raise NotFoundException("课时")
    
    course_id = db_lesson.course_id
    db.delete(db_lesson)
    db.commit()
    
    # 更新课程的总课时数
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course:
        course.total_lessons = db.query(models.Lesson).filter(
            models.Lesson.course_id == course_id
        ).count()
        db.commit()
    
    return {"message": "Lesson deleted successfully"}

# ====== 视频上传 ======

@router.post("/upload/video")
async def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """上传视频文件"""
    # 扩展支持的视频格式
    allowed_types = [
        "video/mp4", "video/avi", "video/mov", "video/wmv", 
        "video/mkv", "video/flv", "video/webm", "video/m4v"
    ]
    allowed_extensions = [".mp4", ".avi", ".mov", ".wmv", ".mkv", ".flv", ".webm", ".m4v"]
    
    # 文件名安全检查
    if not file.filename or ".." in file.filename or "/" in file.filename:
        raise ValidationException("文件名无效")
    
    # 检查文件扩展名
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise UnsupportedFileTypeException(f"支持的格式：{', '.join(allowed_extensions)}")
    
    # 检查MIME类型
    if file.content_type not in allowed_types:
        raise UnsupportedFileTypeException(f"支持的格式：{', '.join(allowed_types)}")
    
    # 检查文件大小（限制为1GB）
    max_size = 1024 * 1024 * 1024  # 1GB
    content = await file.read()
    file_size = len(content)
    
    if file_size == 0:
        raise ValidationException("文件不能为空")
    
    if file_size > max_size:
        raise FileTooLargeException("1GB")
    
    # 生成安全的文件名
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # 创建按日期分组的上传目录
    from datetime import datetime
    date_path = datetime.now().strftime("%Y/%m")
    upload_dir = f"uploads/videos/{date_path}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, unique_filename)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise DatabaseException(f"文件保存失败: {str(e)}")
    
    # 计算文件哈希（用于防重复）
    import hashlib
    file_hash = hashlib.md5(content).hexdigest()
    
    # 记录文件上传日志
    log_file_upload(current_user, file.filename, file_size, file.content_type)
    
    # 返回文件信息
    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "file_path": file_path,
        "file_size": file_size,
        "file_hash": file_hash,
        "content_type": file.content_type,
        "upload_url": f"/uploads/videos/{date_path}/{unique_filename}",
        "uploaded_by": current_user.username,
        "uploaded_at": datetime.now().isoformat()
    }

@router.post("/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """上传图片文件"""
    # 扩展支持的图片格式
    allowed_types = [
        "image/jpeg", "image/jpg", "image/png", "image/gif", 
        "image/webp", "image/bmp", "image/tiff"
    ]
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif"]
    
    # 文件名安全检查
    if not file.filename or ".." in file.filename or "/" in file.filename:
        raise ValidationException("文件名无效")
    
    # 检查文件扩展名
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise UnsupportedFileTypeException(f"支持的格式：{', '.join(allowed_extensions)}")
    
    # 检查MIME类型
    if file.content_type not in allowed_types:
        raise UnsupportedFileTypeException(f"支持的格式：{', '.join(allowed_types)}")
    
    # 检查文件大小（限制为20MB）
    max_size = 20 * 1024 * 1024  # 20MB
    content = await file.read()
    file_size = len(content)
    
    if file_size == 0:
        raise ValidationException("文件不能为空")
    
    if file_size > max_size:
        raise FileTooLargeException("20MB")
    
    # 生成安全的文件名
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # 创建按日期分组的上传目录
    from datetime import datetime
    date_path = datetime.now().strftime("%Y/%m")
    upload_dir = f"uploads/images/{date_path}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, unique_filename)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise DatabaseException(f"文件保存失败: {str(e)}")
    
    # 计算文件哈希
    import hashlib
    file_hash = hashlib.md5(content).hexdigest()
    
    # 获取图片尺寸（如果可能）
    image_info = {}
    try:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(content))
        image_info = {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode
        }
    except ImportError:
        # PIL未安装，跳过图片信息获取
        pass
    except Exception:
        # 图片解析失败，跳过
        pass
    
    # 记录文件上传日志
    log_file_upload(current_user, file.filename, file_size, file.content_type)
    
    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "file_path": file_path,
        "file_size": file_size,
        "file_hash": file_hash,
        "content_type": file.content_type,
        "upload_url": f"/uploads/images/{date_path}/{unique_filename}",
        "uploaded_by": current_user.username,
        "uploaded_at": datetime.now().isoformat(),
        **image_info
    }

@router.post("/upload/document")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """上传文档文件"""
    # 支持的文档格式
    allowed_types = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/plain",
        "text/csv"
    ]
    allowed_extensions = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".csv"]
    
    # 文件名安全检查
    if not file.filename or ".." in file.filename or "/" in file.filename:
        raise ValidationException("文件名无效")
    
    # 检查文件扩展名
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise UnsupportedFileTypeException(f"支持的格式：{', '.join(allowed_extensions)}")
    
    # 检查MIME类型
    if file.content_type not in allowed_types:
        raise UnsupportedFileTypeException(f"支持的格式：{', '.join(allowed_types)}")
    
    # 检查文件大小（限制为50MB）
    max_size = 50 * 1024 * 1024  # 50MB
    content = await file.read()
    file_size = len(content)
    
    if file_size == 0:
        raise ValidationException("文件不能为空")
    
    if file_size > max_size:
        raise FileTooLargeException("50MB")
    
    # 生成安全的文件名
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # 创建按日期分组的上传目录
    from datetime import datetime
    date_path = datetime.now().strftime("%Y/%m")
    upload_dir = f"uploads/documents/{date_path}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, unique_filename)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise DatabaseException(f"文件保存失败: {str(e)}")
    
    # 计算文件哈希
    import hashlib
    file_hash = hashlib.md5(content).hexdigest()
    
    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "file_path": file_path,
        "file_size": file_size,
        "file_hash": file_hash,
        "content_type": file.content_type,
        "upload_url": f"/uploads/documents/{date_path}/{unique_filename}",
        "uploaded_by": current_user.username,
        "uploaded_at": datetime.now().isoformat()
    }

# ====== 统计数据 ======

@router.get("/statistics")
def get_statistics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取平台统计数据"""
    from datetime import datetime, timedelta
    from sqlalchemy import func
    from app.models.user import UserRole, UserStatus
    
    # 基础统计
    total_courses = db.query(models.Course).count()
    published_courses = db.query(models.Course).filter(models.Course.is_published == True).count()
    total_lessons = db.query(models.Lesson).count()
    total_users = db.query(models.User).count()
    total_enrollments = db.query(models.Enrollment).count()
    
    # 专家统计
    total_experts = db.query(models.Expert).count()
    active_experts = db.query(models.Expert).filter(models.Expert.status == ExpertStatus.ACTIVE).count()
    verified_experts = db.query(models.Expert).filter(models.Expert.is_verified == True).count()
    
    # 商品统计
    total_products = db.query(models.Product).count()
    active_products = db.query(models.Product).filter(models.Product.status == ProductStatus.ACTIVE).count()
    featured_products = db.query(models.Product).filter(models.Product.is_featured == True).count()
    
    # 订单统计
    total_orders = db.query(models.Order).count()
    pending_orders = db.query(models.Order).filter(models.Order.status == OrderStatus.PENDING_PAYMENT).count()
    completed_orders = db.query(models.Order).filter(models.Order.status == OrderStatus.DELIVERED).count()
    total_revenue = db.query(func.sum(models.Order.total_amount)).filter(
        models.Order.status.in_([OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED])
    ).scalar() or 0
    
    # 咨询统计
    total_consultations = db.query(models.Consultation).count()
    pending_consultations = db.query(models.Consultation).filter(models.Consultation.status == ConsultationStatus.PENDING).count()
    completed_consultations = db.query(models.Consultation).filter(models.Consultation.status == ConsultationStatus.COMPLETED).count()
    ai_consultations = db.query(models.Consultation).filter(models.Consultation.type == ConsultationType.AI).count()
    expert_consultations = db.query(models.Consultation).filter(models.Consultation.type.in_([ConsultationType.TEXT, ConsultationType.VOICE, ConsultationType.VIDEO])).count()
    
    # 用户分析
    active_users = db.query(models.User).filter(models.User.status == UserStatus.ACTIVE).count()
    vip_users = db.query(models.User).filter(models.User.role == UserRole.VIP).count()
    doctor_users = db.query(models.User).filter(models.User.role == UserRole.DOCTOR).count()
    admin_users = db.query(models.User).filter(models.User.role.in_([UserRole.ADMIN, UserRole.SUPER_ADMIN])).count()
    
    # 课程分析
    free_courses = db.query(models.Course).filter(models.Course.is_free == True).count()
    paid_courses = db.query(models.Course).filter(models.Course.is_free == False).count()
    
    # 最近7天统计
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    new_users_week = db.query(models.User).filter(models.User.created_at >= seven_days_ago).count()
    new_courses_week = db.query(models.Course).filter(models.Course.created_at >= seven_days_ago).count()
    new_enrollments_week = db.query(models.Enrollment).filter(models.Enrollment.enrolled_at >= seven_days_ago).count()
    new_orders_week = db.query(models.Order).filter(models.Order.created_at >= seven_days_ago).count()
    new_consultations_week = db.query(models.Consultation).filter(models.Consultation.created_at >= seven_days_ago).count()
    weekly_revenue = db.query(func.sum(models.Order.total_amount)).filter(
        models.Order.created_at >= seven_days_ago,
        models.Order.status.in_([OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED])
    ).scalar() or 0
    
    # 最近30天统计
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    monthly_revenue = db.query(func.sum(models.Order.total_amount)).filter(
        models.Order.created_at >= thirty_days_ago,
        models.Order.status.in_([OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED])
    ).scalar() or 0
    monthly_orders = db.query(models.Order).filter(models.Order.created_at >= thirty_days_ago).count()
    monthly_consultations = db.query(models.Consultation).filter(models.Consultation.created_at >= thirty_days_ago).count()
    
    # 学习进度统计
    total_watch_time = db.query(func.sum(models.WatchRecord.watch_time)).scalar() or 0
    completed_lessons = db.query(models.WatchRecord).filter(models.WatchRecord.is_completed == True).count()
    
    # 商品分类统计
    from app.models.product import ProductCategory
    product_category_stats = {}
    for category in ProductCategory:
        count = db.query(models.Product).filter(models.Product.category == category).count()
        product_category_stats[category.value] = count
    
    # 专家分类统计
    from app.models.expert import ExpertCategory
    expert_category_stats = {}
    for category in ExpertCategory:
        count = db.query(models.Expert).filter(models.Expert.category == category).count()
        expert_category_stats[category.value] = count
    
    return {
        "overview": {
            "total_users": total_users,
            "total_experts": total_experts,
            "total_products": total_products,
            "total_courses": total_courses,
            "total_orders": total_orders,
            "total_consultations": total_consultations,
            "total_revenue": round(total_revenue, 2)
        },
        "expert_stats": {
            "total_experts": total_experts,
            "active_experts": active_experts,
            "verified_experts": verified_experts,
            "category_stats": expert_category_stats
        },
        "product_stats": {
            "total_products": total_products,
            "active_products": active_products,
            "featured_products": featured_products,
            "category_stats": product_category_stats
        },
        "order_stats": {
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "completion_rate": round(completed_orders / max(total_orders, 1) * 100, 2),
            "total_revenue": round(total_revenue, 2)
        },
        "consultation_stats": {
            "total_consultations": total_consultations,
            "pending_consultations": pending_consultations,
            "completed_consultations": completed_consultations,
            "ai_consultations": ai_consultations,
            "expert_consultations": expert_consultations,
            "completion_rate": round(completed_consultations / max(total_consultations, 1) * 100, 2)
        },
        "user_analysis": {
            "active_users": active_users,
            "vip_users": vip_users,
            "doctor_users": doctor_users,
            "admin_users": admin_users,
            "user_distribution": {
                "regular": total_users - vip_users - doctor_users - admin_users,
                "vip": vip_users,
                "doctor": doctor_users,
                "admin": admin_users
            }
        },
        "course_analysis": {
            "total_courses": total_courses,
            "published_courses": published_courses,
            "free_courses": free_courses,
            "paid_courses": paid_courses,
            "total_lessons": total_lessons,
            "total_enrollments": total_enrollments
        },
        "recent_activity": {
            "last_7_days": {
                "new_users": new_users_week,
                "new_courses": new_courses_week,
                "new_enrollments": new_enrollments_week,
                "new_orders": new_orders_week,
                "new_consultations": new_consultations_week,
                "revenue": round(weekly_revenue, 2)
            },
            "last_30_days": {
                "revenue": round(monthly_revenue, 2),
                "orders": monthly_orders,
                "consultations": monthly_consultations
            }
        },
        "learning_stats": {
            "total_watch_time_hours": round(total_watch_time / 3600, 2),
            "completed_lessons": completed_lessons,
            "avg_completion_rate": round(completed_lessons / max(total_enrollments, 1) * 100, 2)
        }
    }

# ====== 专家管理 ======

@router.get("/experts")
def get_all_experts(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取所有专家"""
    query = db.query(models.Expert)
    
    if status:
        query = query.filter(models.Expert.status == status)
    if category:
        query = query.filter(models.Expert.category == category)
    
    experts = query.offset(skip).limit(limit).all()
    return experts

@router.post("/experts")
def create_expert(
    expert_data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """创建新专家"""
    db_expert = models.Expert(**expert_data)
    db.add(db_expert)
    db.commit()
    db.refresh(db_expert)
    
    log_admin_action(current_user, "创建专家", f"专家ID:{db_expert.id}", f"专家姓名:{db_expert.name}")
    return db_expert

@router.put("/experts/{expert_id}")
def update_expert(
    expert_id: int,
    expert_data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """更新专家信息"""
    expert = db.query(models.Expert).filter(models.Expert.id == expert_id).first()
    if not expert:
        raise CommonErrors.EXPERT_NOT_FOUND
    
    for field, value in expert_data.items():
        if hasattr(expert, field):
            setattr(expert, field, value)
    
    db.commit()
    db.refresh(expert)
    return expert

@router.delete("/experts/{expert_id}")
def delete_expert(
    expert_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """删除专家"""
    expert = db.query(models.Expert).filter(models.Expert.id == expert_id).first()
    if not expert:
        raise CommonErrors.EXPERT_NOT_FOUND
    
    expert_name = expert.name
    db.delete(expert)
    db.commit()
    
    log_admin_action(current_user, "删除专家", f"专家ID:{expert_id}", f"专家姓名:{expert_name}")
    return {"message": "专家删除成功"}

@router.get("/experts/{expert_id}/reviews")
def get_expert_reviews(
    expert_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取专家评价"""
    reviews = db.query(models.ExpertReview).filter(
        models.ExpertReview.expert_id == expert_id
    ).offset(skip).limit(limit).all()
    return reviews

@router.get("/experts/{expert_id}/schedules")
def get_expert_schedules(
    expert_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取专家排班"""
    query = db.query(models.ExpertSchedule).filter(
        models.ExpertSchedule.expert_id == expert_id
    )
    
    if start_date:
        query = query.filter(models.ExpertSchedule.date >= start_date)
    if end_date:
        query = query.filter(models.ExpertSchedule.date <= end_date)
    
    schedules = query.all()
    return schedules

# ====== 商品管理 ======

@router.get("/products")
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取所有商品"""
    query = db.query(models.Product)
    
    if category:
        query = query.filter(models.Product.category == category)
    if status:
        query = query.filter(models.Product.status == status)
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.post("/products", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """创建新商品"""
    # 使用model_dump(mode='json')来获取数据，确保枚举被序列化为字符串
    product_data = product.model_dump(mode='json')
    product_data['audit_status'] = AuditStatus.APPROVED  # 管理员创建的产品直接审核通过
    
    db_product = models.Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    log_admin_action(current_user, "创建商品", f"商品ID:{db_product.id}", f"商品名称:{db_product.name}")
    return db_product

@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """更新商品信息"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise CommonErrors.PRODUCT_NOT_FOUND
    
    # 更新商品信息
    for field, value in product_update.model_dump(exclude_unset=True, mode='json').items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """删除商品"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise CommonErrors.PRODUCT_NOT_FOUND
    
    product_name = product.name
    db.delete(product)
    db.commit()
    
    log_admin_action(current_user, "删除商品", f"商品ID:{product_id}", f"商品名称:{product_name}")
    return {"message": "商品删除成功"}

# ====== 订单管理 ======

@router.get("/orders")
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取所有订单"""
    query = db.query(models.Order)
    
    if status:
        query = query.filter(models.Order.status == status)
    
    orders = query.offset(skip).limit(limit).all()
    return orders

@router.get("/orders/{order_id}")
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取订单详情"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise CommonErrors.ORDER_NOT_FOUND
    return order

@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    tracking_number: Optional[str] = None,
    courier_company: Optional[str] = None,
    admin_note: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """更新订单状态"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise CommonErrors.ORDER_NOT_FOUND
    
    old_status = order.status
    order.status = status
    
    if tracking_number:
        order.tracking_number = tracking_number
    if courier_company:
        order.courier_company = courier_company
    if admin_note:
        order.admin_note = admin_note
    
    # 设置状态变更时间
    if status == OrderStatus.SHIPPED:
        order.shipped_at = datetime.now()
    elif status == OrderStatus.DELIVERED:
        order.delivered_at = datetime.now()
    
    db.commit()
    
    log_admin_action(
        current_user, 
        "更新订单状态", 
        f"订单号:{order.order_number}", 
        f"从 {old_status} 变更为 {status}"
    )
    return {"message": "订单状态更新成功"}

# ====== 咨询管理 ======

@router.get("/consultations")
def get_all_consultations(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    type: Optional[str] = None,
    expert_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取所有咨询记录"""
    query = db.query(models.Consultation)
    
    if status:
        query = query.filter(models.Consultation.status == status)
    if type:
        query = query.filter(models.Consultation.type == type)
    if expert_id:
        query = query.filter(models.Consultation.expert_id == expert_id)
    
    consultations = query.offset(skip).limit(limit).all()
    return consultations

@router.get("/consultations/{consultation_id}")
def get_consultation_detail(
    consultation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取咨询详情"""
    consultation = db.query(models.Consultation).filter(
        models.Consultation.id == consultation_id
    ).first()
    if not consultation:
        raise NotFoundException("咨询记录")
    return consultation

@router.put("/consultations/{consultation_id}")
def update_consultation(
    consultation_id: int,
    consultation_data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """更新咨询信息"""
    consultation = db.query(models.Consultation).filter(
        models.Consultation.id == consultation_id
    ).first()
    if not consultation:
        raise NotFoundException("咨询记录")
    
    for field, value in consultation_data.items():
        if hasattr(consultation, field):
            setattr(consultation, field, value)
    
    db.commit()
    db.refresh(consultation)
    return consultation

@router.get("/consultations/{consultation_id}/messages")
def get_consultation_messages(
    consultation_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取咨询消息记录"""
    messages = db.query(models.ConsultationMessage).filter(
        models.ConsultationMessage.consultation_id == consultation_id
    ).offset(skip).limit(limit).all()
    return messages

# ====== 用户管理 ======

@router.get("/users")
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取所有用户"""
    from app.core.response import ApiResponse, user_to_dict
    
    users = db.query(models.User).offset(skip).limit(limit).all()
    user_list = [user_to_dict(user) for user in users]
    
    return {"success": True, "data": user_list, "message": "用户列表获取成功"}

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    is_admin: bool = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """更新用户权限"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise CommonErrors.USER_NOT_FOUND
    
    user.is_admin = is_admin
    db.commit()
    
    return {"message": f"User role updated successfully"}

# ====== 数据导出 ======

@router.get("/export/users")
def export_users(
    format: str = "csv",  # csv, json
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """导出用户数据"""
    users = db.query(models.User).all()
    
    # 记录数据导出日志
    log_data_export(current_user, f"用户数据({format})", len(users))
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        
        # CSV表头
        writer.writerow([
            "ID", "用户名", "邮箱", "姓名", "电话", "角色", "状态", 
            "是否激活", "注册时间", "最后登录"
        ])
        
        # 数据行
        for user in users:
            writer.writerow([
                user.id, user.username, user.email, user.full_name or "",
                user.phone or "", user.role.value, user.status.value,
                "是" if user.is_active else "否",
                user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else "",
                user.last_login.strftime("%Y-%m-%d %H:%M:%S") if hasattr(user, 'last_login') and user.last_login else ""
            ])
        
        output.seek(0)
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
    
    else:  # JSON格式
        user_data = []
        for user in users:
            user_data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "phone": user.phone,
                "role": user.role.value,
                "status": user.status.value,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None
            })
        
        return user_data

@router.get("/export/courses")
def export_courses(
    format: str = "csv",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """导出课程数据"""
    courses = db.query(models.Course).all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        
        # CSV表头
        writer.writerow([
            "ID", "标题", "描述", "分类", "讲师", "时长", "价格", 
            "是否免费", "是否发布", "总课时", "创建时间"
        ])
        
        # 数据行
        for course in courses:
            writer.writerow([
                course.id, course.title, course.description or "",
                course.category.value, course.instructor or "", course.duration or "",
                course.price or 0, "是" if course.is_free else "否",
                "是" if course.is_published else "否", course.total_lessons or 0,
                course.created_at.strftime("%Y-%m-%d %H:%M:%S") if course.created_at else ""
            ])
        
        output.seek(0)
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=courses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
    
    else:  # JSON格式
        course_data = []
        for course in courses:
            course_data.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "category": course.category.value,
                "instructor": course.instructor,
                "duration": course.duration,
                "price": course.price,
                "is_free": course.is_free,
                "is_published": course.is_published,
                "total_lessons": course.total_lessons,
                "created_at": course.created_at.isoformat() if course.created_at else None
            })
        
        return course_data

@router.get("/export/enrollments")
def export_enrollments(
    format: str = "csv",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """导出注册数据"""
    from sqlalchemy.orm import joinedload
    
    enrollments = db.query(models.Enrollment).options(
        joinedload(models.Enrollment.course)
    ).all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        
        # CSV表头
        writer.writerow([
            "ID", "用户ID", "课程ID", "课程标题", "学习进度(%)", 
            "已完成课时", "总观看时长(小时)", "注册时间", "完成时间"
        ])
        
        # 数据行
        for enrollment in enrollments:
            writer.writerow([
                enrollment.id, enrollment.user_id, enrollment.course_id,
                enrollment.course.title if enrollment.course else "",
                round(enrollment.progress * 100, 2) if enrollment.progress else 0,
                enrollment.completed_lessons or 0,
                round((enrollment.total_watch_time or 0) / 3600, 2),
                enrollment.enrolled_at.strftime("%Y-%m-%d %H:%M:%S") if enrollment.enrolled_at else "",
                enrollment.completed_at.strftime("%Y-%m-%d %H:%M:%S") if enrollment.completed_at else ""
            ])
        
        output.seek(0)
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=enrollments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
    
    else:  # JSON格式
        enrollment_data = []
        for enrollment in enrollments:
            enrollment_data.append({
                "id": enrollment.id,
                "user_id": enrollment.user_id,
                "course_id": enrollment.course_id,
                "course_title": enrollment.course.title if enrollment.course else None,
                "progress": enrollment.progress,
                "completed_lessons": enrollment.completed_lessons,
                "total_watch_time": enrollment.total_watch_time,
                "enrolled_at": enrollment.enrolled_at.isoformat() if enrollment.enrolled_at else None,
                "completed_at": enrollment.completed_at.isoformat() if enrollment.completed_at else None
            })
        
        return enrollment_data

# ====== 系统管理 ======

@router.post("/system/backup")
def create_backup(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """创建系统数据备份"""
    import shutil
    from datetime import datetime
    
    # 创建备份目录
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # 生成备份文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{timestamp}.sqlite"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # 复制数据库文件
        shutil.copy2("./database.db", backup_path)
        
        return {
            "message": "备份创建成功",
            "backup_file": backup_filename,
            "backup_path": backup_path,
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise DatabaseException(f"备份创建失败: {str(e)}")

@router.get("/system/logs")
def get_system_logs(
    lines: int = 100,
    current_user: models.User = Depends(require_admin_role)
):
    """获取系统日志"""
    log_file = "app.log"
    
    if not os.path.exists(log_file):
        return {"logs": [], "message": "日志文件不存在"}
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        return {
            "logs": [line.strip() for line in recent_lines],
            "total_lines": len(all_lines),
            "showing_lines": len(recent_lines)
        }
    except Exception as e:
        raise DatabaseException(f"读取日志失败: {str(e)}")

# ====== 审核管理 ======

class AuditRequest(BaseModel):
    """审核请求模型"""
    action: str  # approve, reject, publish, offline
    reason: Optional[str] = None  # 审核意见
    notes: Optional[str] = None   # 备注

@router.get("/audit/pending")
def get_pending_audits(
    entity_type: Optional[str] = None,  # course, expert, product
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取待审核列表"""
    from app.core.response import ApiResponse
    
    try:
        result = {}
        
        # 确定要查询的实体类型
        entity_types = [entity_type] if entity_type else ['course', 'expert', 'product']
        
        for entity in entity_types:
            if entity == 'course':
                items = db.query(models.Course).filter(
                    models.Course.audit_status == AuditStatus.PENDING
                ).offset(skip).limit(limit).all()
            elif entity == 'expert':
                items = db.query(models.Expert).filter(
                    models.Expert.audit_status == AuditStatus.PENDING
                ).offset(skip).limit(limit).all()
            elif entity == 'product':
                items = db.query(models.Product).filter(
                    models.Product.audit_status == AuditStatus.PENDING
                ).offset(skip).limit(limit).all()
            else:
                continue
                
            # 转换为字典格式，便于前端使用
            items_data = []
            for item in items:
                item_data = {
                    'id': item.id,
                    'title': getattr(item, 'title', None) or getattr(item, 'name', '未知'),
                    'submitted_by': item.submitted_by,
                    'submitted_at': item.submitted_at.isoformat() if item.submitted_at else None,
                    'audit_status': item.audit_status.value,
                    'created_at': item.created_at.isoformat() if item.created_at else None
                }
                
                # 添加实体特有字段
                if entity == 'course':
                    item_data.update({
                        'category': item.category.value,
                        'instructor': item.instructor,
                        'price': float(item.price) if item.price else 0
                    })
                elif entity == 'expert':
                    item_data.update({
                        'category': item.category.value,
                        'level': item.level.value,
                        'hospital_affiliation': item.hospital_affiliation
                    })
                elif entity == 'product':
                    item_data.update({
                        'category': item.category.value,
                        'price': float(item.price) if item.price else 0,
                        'stock_quantity': item.stock_quantity
                    })
                
                items_data.append(item_data)
            
            result[entity] = items_data
        
        return ApiResponse.success(result, "待审核列表获取成功")
        
    except Exception as e:
        return ApiResponse.error(f"获取待审核列表失败: {str(e)}", 500)

@router.post("/audit/{entity_type}/{entity_id}")
def perform_audit(
    entity_type: str,
    entity_id: int,
    audit_request: AuditRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """执行审核操作"""
    from app.core.response import ApiResponse
    
    try:
        # 验证实体类型
        if entity_type not in ['course', 'expert', 'product']:
            return ApiResponse.error("不支持的实体类型", 400)
        
        # 获取实体模型
        model_map = {
            'course': models.Course,
            'expert': models.Expert,
            'product': models.Product
        }
        
        Model = model_map[entity_type]
        entity = db.query(Model).filter(Model.id == entity_id).first()
        
        if not entity:
            return ApiResponse.error(f"{entity_type} 不存在", 404)
        
        # 获取当前状态
        old_status = entity.audit_status
        
        # 状态转换逻辑
        if audit_request.action == 'approve':
            if old_status != AuditStatus.PENDING:
                return ApiResponse.error("只能审核待审核状态的项目", 400)
            new_status = AuditStatus.APPROVED
            
        elif audit_request.action == 'reject':
            if old_status != AuditStatus.PENDING:
                return ApiResponse.error("只能审核待审核状态的项目", 400)
            new_status = AuditStatus.REJECTED
            
        elif audit_request.action == 'publish':
            if old_status != AuditStatus.APPROVED:
                return ApiResponse.error("只能发布已通过审核的项目", 400)
            new_status = AuditStatus.PUBLISHED
            
        elif audit_request.action == 'offline':
            if old_status != AuditStatus.PUBLISHED:
                return ApiResponse.error("只能下架已发布的项目", 400)
            new_status = AuditStatus.OFFLINE
            
        else:
            return ApiResponse.error("无效的审核操作", 400)
        
        # 更新实体状态
        entity.audit_status = new_status
        entity.reviewed_by = current_user.username
        entity.reviewed_at = datetime.now()
        if audit_request.notes:
            entity.audit_notes = audit_request.notes
        
        # 创建审核日志
        audit_log = models.AuditLog(
            entity_type=entity_type,
            entity_id=entity_id,
            entity_title=getattr(entity, 'title', None) or getattr(entity, 'name', '未知'),
            action=audit_request.action,
            old_status=old_status.value,
            new_status=new_status.value,
            operator_id=current_user.id,
            operator_name=current_user.username,
            operator_role=current_user.role.value,
            reason=audit_request.reason,
            attachment={'notes': audit_request.notes} if audit_request.notes else None
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(entity)
        
        # 记录管理员操作日志
        log_admin_action(
            current_user,
            f"审核{entity_type}",
            f"ID:{entity_id}",
            f"{old_status.value} -> {new_status.value}"
        )
        
        return ApiResponse.success({
            'entity_id': entity_id,
            'entity_type': entity_type,
            'old_status': old_status.value,
            'new_status': new_status.value,
            'action': audit_request.action
        }, "审核操作成功")
        
    except Exception as e:
        db.rollback()
        return ApiResponse.error(f"审核操作失败: {str(e)}", 500)

@router.get("/audit/logs/{entity_type}/{entity_id}")
def get_audit_logs(
    entity_type: str,
    entity_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取实体的审核历史"""
    from app.core.response import ApiResponse
    
    try:
        logs = db.query(models.AuditLog).filter(
            models.AuditLog.entity_type == entity_type,
            models.AuditLog.entity_id == entity_id
        ).order_by(models.AuditLog.created_at.desc()).offset(skip).limit(limit).all()
        
        logs_data = []
        for log in logs:
            logs_data.append({
                'id': log.id,
                'action': log.action,
                'action_description': log.action_description,
                'old_status': log.old_status,
                'new_status': log.new_status,
                'operator_name': log.operator_name,
                'operator_role': log.operator_role,
                'reason': log.reason,
                'attachment': log.attachment,
                'created_at': log.created_at.isoformat()
            })
        
        return ApiResponse.success(logs_data, "审核历史获取成功")
        
    except Exception as e:
        return ApiResponse.error(f"获取审核历史失败: {str(e)}", 500)

@router.get("/audit/stats")
def get_audit_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取审核统计数据"""
    from app.core.response import ApiResponse
    from sqlalchemy import func
    
    try:
        stats = {}
        
        # 统计各实体类型的审核状态分布
        for entity_type, Model in [('course', models.Course), ('expert', models.Expert), ('product', models.Product)]:
            # 按状态统计数量
            status_stats = db.query(
                Model.audit_status,
                func.count(Model.id)
            ).group_by(Model.audit_status).all()
            
            stats[entity_type] = {}
            for status, count in status_stats:
                stats[entity_type][status.value] = count
        
        # 最近7天的审核活动
        from datetime import timedelta
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        recent_logs = db.query(models.AuditLog).filter(
            models.AuditLog.created_at >= seven_days_ago
        ).all()
        
        recent_stats = {
            'total_actions': len(recent_logs),
            'by_action': {},
            'by_operator': {}
        }
        
        # 按操作类型统计
        for log in recent_logs:
            recent_stats['by_action'][log.action] = recent_stats['by_action'].get(log.action, 0) + 1
            recent_stats['by_operator'][log.operator_name] = recent_stats['by_operator'].get(log.operator_name, 0) + 1
        
        return ApiResponse.success({
            'entity_stats': stats,
            'recent_activity': recent_stats
        }, "审核统计获取成功")
        
    except Exception as e:
        return ApiResponse.error(f"获取审核统计失败: {str(e)}", 500)