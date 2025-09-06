"""
课程模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class CourseCategory(str, enum.Enum):
    BASIC = "basic"
    SEASONAL = "seasonal" 
    DIET = "diet"
    MASSAGE = "massage"
    HERB = "herb"
    DISEASE_FOCUSED = "逐病精讲"  # 逐病精讲分类
    COMPREHENSIVE = "全面学医"   # 全面学医分类

class VideoStatus(str, enum.Enum):
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(Enum(CourseCategory), nullable=False)
    duration = Column(String)  # 例如: "10课时"
    price = Column(Float)
    image_url = Column(String)
    is_free = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    instructor = Column(String)  # 讲师名称
    total_lessons = Column(Integer, default=0)  # 总课时数
    total_duration = Column(Integer, default=0)  # 总时长（分钟）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course")

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', category='{self.category}')>"

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)  # 课程顺序
    duration = Column(Integer)  # 视频时长（秒）
    
    # 腾讯云点播相关字段
    video_url = Column(String)  # 视频播放地址
    video_id = Column(String)  # 腾讯云视频ID
    file_id = Column(String)  # 腾讯云文件ID
    cover_url = Column(String)  # 视频封面
    status = Column(Enum(VideoStatus), default=VideoStatus.PROCESSING)
    
    # 其他字段
    is_free = Column(Boolean, default=False)
    transcript = Column(Text)  # 视频字幕/文稿
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    course = relationship("Course", back_populates="lessons")
    watch_records = relationship("WatchRecord", back_populates="lesson")

    def __repr__(self):
        return f"<Lesson(id={self.id}, title='{self.title}', course_id={self.course_id})>"

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    progress = Column(Float, default=0.0)  # 学习进度 0.0-1.0
    completed_lessons = Column(Integer, default=0)  # 已完成课程数
    total_watch_time = Column(Integer, default=0)  # 总观看时长（秒）
    last_watched_lesson_id = Column(Integer, ForeignKey("lessons.id"))
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    # 关系
    course = relationship("Course", back_populates="enrollments")

class WatchRecord(Base):
    __tablename__ = "watch_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    watch_time = Column(Integer, default=0)  # 观看时长（秒）
    last_position = Column(Integer, default=0)  # 最后观看位置（秒）
    is_completed = Column(Boolean, default=False)  # 是否看完
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    lesson = relationship("Lesson", back_populates="watch_records")