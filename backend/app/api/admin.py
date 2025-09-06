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
from sqlalchemy.orm import Session
from typing import List, Optional

from app import schemas, models
from app.database import get_db
from app.core.permissions import require_admin_role, get_current_user
from app.core.logger import log_admin_action, log_file_upload, log_data_export, admin_logger

router = APIRouter(tags=["admin"])

# ====== 课程管理 ======

@router.post("/test")
def test_create():
    """测试API端点"""
    admin_logger.logger.info("测试API被调用")
    return {"message": "测试成功"}

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename"
        )
    
    # 检查文件扩展名
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # 检查MIME类型
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # 检查文件大小（限制为1GB）
    max_size = 1024 * 1024 * 1024  # 1GB
    content = await file.read()
    file_size = len(content)
    
    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file not allowed"
        )
    
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 1GB."
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename"
        )
    
    # 检查文件扩展名
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # 检查MIME类型
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # 检查文件大小（限制为20MB）
    max_size = 20 * 1024 * 1024  # 20MB
    content = await file.read()
    file_size = len(content)
    
    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file not allowed"
        )
    
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 20MB."
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename"
        )
    
    # 检查文件扩展名
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # 检查MIME类型
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # 检查文件大小（限制为50MB）
    max_size = 50 * 1024 * 1024  # 50MB
    content = await file.read()
    file_size = len(content)
    
    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file not allowed"
        )
    
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 50MB."
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
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
    active_experts = db.query(models.Expert).filter(models.Expert.status == "active").count()
    verified_experts = db.query(models.Expert).filter(models.Expert.is_verified == True).count()
    
    # 商品统计
    total_products = db.query(models.Product).count()
    active_products = db.query(models.Product).filter(models.Product.status == "active").count()
    featured_products = db.query(models.Product).filter(models.Product.is_featured == True).count()
    
    # 订单统计
    total_orders = db.query(models.Order).count()
    pending_orders = db.query(models.Order).filter(models.Order.status == "pending_payment").count()
    completed_orders = db.query(models.Order).filter(models.Order.status == "delivered").count()
    total_revenue = db.query(func.sum(models.Order.total_amount)).filter(
        models.Order.status.in_(["paid", "shipped", "delivered"])
    ).scalar() or 0
    
    # 咨询统计
    total_consultations = db.query(models.Consultation).count()
    pending_consultations = db.query(models.Consultation).filter(models.Consultation.status == "pending").count()
    completed_consultations = db.query(models.Consultation).filter(models.Consultation.status == "completed").count()
    ai_consultations = db.query(models.Consultation).filter(models.Consultation.type == "ai").count()
    expert_consultations = db.query(models.Consultation).filter(models.Consultation.type.in_(["text", "voice", "video"])).count()
    
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
        models.Order.status.in_(["paid", "shipped", "delivered"])
    ).scalar() or 0
    
    # 最近30天统计
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    monthly_revenue = db.query(func.sum(models.Order.total_amount)).filter(
        models.Order.created_at >= thirty_days_ago,
        models.Order.status.in_(["paid", "shipped", "delivered"])
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
        raise HTTPException(status_code=404, detail="专家未找到")
    
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
        raise HTTPException(status_code=404, detail="专家未找到")
    
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
    # 使用product.dict()来获取数据，并设置默认审核状态
    product_data = product.dict()
    product_data['audit_status'] = 'approved'  # 管理员创建的产品直接审核通过
    
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
        raise HTTPException(status_code=404, detail="商品未找到")
    
    # 更新商品信息
    for field, value in product_update.dict(exclude_unset=True).items():
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
        raise HTTPException(status_code=404, detail="商品未找到")
    
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
        raise HTTPException(status_code=404, detail="订单未找到")
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
        raise HTTPException(status_code=404, detail="订单未找到")
    
    old_status = order.status
    order.status = status
    
    if tracking_number:
        order.tracking_number = tracking_number
    if courier_company:
        order.courier_company = courier_company
    if admin_note:
        order.admin_note = admin_note
    
    # 设置状态变更时间
    if status == "shipped":
        order.shipped_at = datetime.now()
    elif status == "delivered":
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
        raise HTTPException(status_code=404, detail="咨询记录未找到")
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
        raise HTTPException(status_code=404, detail="咨询记录未找到")
    
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

@router.get("/users", response_model=List[schemas.User])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin_role)
):
    """获取所有用户"""
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"备份创建失败: {str(e)}"
        )

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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"读取日志失败: {str(e)}"
        )