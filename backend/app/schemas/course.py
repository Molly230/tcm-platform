"""
课程相关的Pydantic模型
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.core.enums_v2 import CourseCategory, VideoStatus

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: CourseCategory
    duration: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_free: bool = False
    is_published: bool = False
    instructor: Optional[str] = None
    total_lessons: int = 0
    total_duration: int = 0

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[CourseCategory] = None
    duration: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_free: Optional[bool] = None
    is_published: Optional[bool] = None
    instructor: Optional[str] = None

class LessonBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    order: int
    duration: Optional[int] = None
    video_url: Optional[str] = None
    video_id: Optional[str] = None
    file_id: Optional[str] = None
    cover_url: Optional[str] = None
    status: VideoStatus = VideoStatus.PROCESSING
    is_free: bool = False
    transcript: Optional[str] = None

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    duration: Optional[int] = None
    video_url: Optional[str] = None
    video_id: Optional[str] = None
    file_id: Optional[str] = None
    cover_url: Optional[str] = None
    status: Optional[VideoStatus] = None
    is_free: Optional[bool] = None
    transcript: Optional[str] = None

class Lesson(LessonBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    lessons: List[Lesson] = []

    class Config:
        from_attributes = True

class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
    progress: float = 0.0
    completed_lessons: int = 0
    total_watch_time: int = 0
    last_watched_lesson_id: Optional[int] = None
    enrolled_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WatchRecordBase(BaseModel):
    user_id: int
    lesson_id: int
    watch_time: int = 0
    last_position: int = 0
    is_completed: bool = False

class WatchRecordCreate(WatchRecordBase):
    pass

class WatchRecordUpdate(BaseModel):
    watch_time: Optional[int] = None
    last_position: Optional[int] = None
    is_completed: Optional[bool] = None

class WatchRecord(WatchRecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True