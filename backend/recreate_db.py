#!/usr/bin/env python3
"""
重新创建数据库和测试数据
"""
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, Base
from app.models import *  # 导入所有模型

def recreate_database():
    """重新创建数据库"""
    
    # 删除所有表
    Base.metadata.drop_all(bind=engine)
    print("已删除所有数据表")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("已重新创建所有数据表")
    
    db = SessionLocal()
    
    try:
        # 1. 创建测试用户
        from app.models.user import User
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashedpassword123"
        )
        db.add(user)
        db.flush()
        
        # 2. 创建基础课程
        from app.models.course import Course, Lesson, CourseCategory, VideoStatus
        basic_course = Course(
            title="中医养生基础课程",
            description="学习中医养生的基本理论和实践方法",
            category=CourseCategory.BASIC,
            duration="3课时",
            price=99.0,
            is_free=False,
            is_published=True,
            instructor="张医师",
            total_lessons=3,
            total_duration=1800
        )
        db.add(basic_course)
        db.flush()
        
        # 基础课程的课时
        basic_lessons = [
            {
                "title": "第一课：中医基础理论",
                "description": "介绍中医的基本理论体系",
                "order": 1,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
                "is_free": True
            },
            {
                "title": "第二课：经络与穴位",
                "description": "了解人体经络系统和重要穴位",
                "order": 2,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4",
                "is_free": False
            },
            {
                "title": "第三课：养生实践方法",
                "description": "日常养生的具体方法和注意事项",
                "order": 3,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_5mb.mp4",
                "is_free": False
            }
        ]
        
        for lesson_data in basic_lessons:
            lesson = Lesson(
                course_id=basic_course.id,
                **lesson_data,
                video_id=f"basic_video_{lesson_data['order']}",
                file_id=f"file_basic_{lesson_data['order']}",
                cover_url=f"https://via.placeholder.com/640x360/4CAF50/FFFFFF?text=第{lesson_data['order']}课",
                status=VideoStatus.READY
            )
            db.add(lesson)
        
        # 3. 逐病精讲 - 失眠专题
        insomnia_course = Course(
            title="逐病精讲：失眠调理专题",
            description="深入讲解失眠的中医病因病机，详细介绍针灸、药膳、按摩等多种调理方法，让你彻底告别失眠困扰。",
            category=CourseCategory.DISEASE_FOCUSED,
            duration="8课时",
            price=199.0,
            image_url="https://via.placeholder.com/400x250/E3F2FD/1976D2?text=失眠调理专题",
            is_free=False,
            is_published=True,
            instructor="王安宁教授",
            total_lessons=4,
            total_duration=2400
        )
        db.add(insomnia_course)
        db.flush()
        
        # 失眠课程的课时
        insomnia_lessons = [
            {
                "title": "第1课：失眠的中医认识",
                "description": "了解失眠在中医理论中的病因病机分析",
                "order": 1,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
                "is_free": True
            },
            {
                "title": "第2课：失眠的辨证分型",
                "description": "学习不同类型失眠的中医辨证方法",
                "order": 2,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4",
                "is_free": False
            },
            {
                "title": "第3课：安神药膳调理",
                "description": "掌握治疗失眠的经典药膳配方",
                "order": 3,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_3mb.mp4",
                "is_free": False
            },
            {
                "title": "第4课：失眠的针灸治疗",
                "description": "学习治疗失眠的有效针灸穴位和手法",
                "order": 4,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_4mb.mp4",
                "is_free": False
            }
        ]
        
        for lesson_data in insomnia_lessons:
            lesson = Lesson(
                course_id=insomnia_course.id,
                **lesson_data,
                video_id=f"insomnia_video_{lesson_data['order']}",
                file_id=f"file_insomnia_{lesson_data['order']}",
                cover_url=f"https://via.placeholder.com/640x360/E3F2FD/1976D2?text=失眠第{lesson_data['order']}课",
                status=VideoStatus.READY
            )
            db.add(lesson)
        
        # 4. 逐病精讲 - 胃病专题
        gastric_course = Course(
            title="逐病精讲：胃病调理专题", 
            description="从中医角度全面解析胃病成因，传授脾胃调理的实用方法，包括饮食调护、穴位按摩、中药调理等。",
            category=CourseCategory.DISEASE_FOCUSED,
            duration="10课时",
            price=249.0,
            image_url="https://via.placeholder.com/400x250/FFF3E0/F57C00?text=胃病调理专题",
            is_free=False,
            is_published=True,
            instructor="李消化主任",
            total_lessons=4,
            total_duration=2400
        )
        db.add(gastric_course)
        db.flush()
        
        # 胃病课程的课时
        gastric_lessons = [
            {
                "title": "第1课：脾胃在中医中的地位",
                "description": "理解脾胃为后天之本的中医理论",
                "order": 1,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
                "is_free": True
            },
            {
                "title": "第2课：常见胃病的中医分型",
                "description": "学习胃炎、胃溃疡等的中医辨证",
                "order": 2,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4", 
                "is_free": False
            },
            {
                "title": "第3课：养胃护胃的饮食原则",
                "description": "掌握科学的养胃饮食方法",
                "order": 3,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_3mb.mp4",
                "is_free": False
            },
            {
                "title": "第4课：胃病的穴位调理",
                "description": "学习治疗胃病的重要穴位和按摩方法",
                "order": 4,
                "duration": 600,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_4mb.mp4",
                "is_free": False
            }
        ]
        
        for lesson_data in gastric_lessons:
            lesson = Lesson(
                course_id=gastric_course.id,
                **lesson_data,
                video_id=f"gastric_video_{lesson_data['order']}",
                file_id=f"file_gastric_{lesson_data['order']}",
                cover_url=f"https://via.placeholder.com/640x360/FFF3E0/F57C00?text=胃病第{lesson_data['order']}课",
                status=VideoStatus.READY
            )
            db.add(lesson)
        
        # 5. 全面学医系列课程
        comprehensive_course = Course(
            title="全面学医：中医入门到精通",
            description="系统学习中医理论体系，从基础理论到临床应用，培养扎实的中医思维和实践能力。适合零基础学员。",
            category=CourseCategory.COMPREHENSIVE,
            duration="50课时",
            price=999.0,
            image_url="https://via.placeholder.com/400x250/E8F5E8/388E3C?text=全面学医系列",
            is_free=False,
            is_published=True,
            instructor="张仲景传人",
            total_lessons=4,
            total_duration=3600
        )
        db.add(comprehensive_course)
        db.flush()
        
        # 全面学医课程的前几课
        comprehensive_lessons = [
            {
                "title": "第1课：中医学概述",
                "description": "了解中医学的历史发展和基本特点",
                "order": 1,
                "duration": 900,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
                "is_free": True
            },
            {
                "title": "第2课：阴阳五行学说",
                "description": "深入理解中医基础理论中的阴阳五行",
                "order": 2,
                "duration": 900,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4",
                "is_free": True  # 前两课免费试听
            },
            {
                "title": "第3课：脏腑经络理论",
                "description": "学习五脏六腑和经络系统的理论",
                "order": 3,
                "duration": 900,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_3mb.mp4",
                "is_free": False
            },
            {
                "title": "第4课：气血津液学说",
                "description": "掌握气血津液的生理功能和病理变化",
                "order": 4,
                "duration": 900,
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_4mb.mp4",
                "is_free": False
            }
        ]
        
        for lesson_data in comprehensive_lessons:
            lesson = Lesson(
                course_id=comprehensive_course.id,
                **lesson_data,
                video_id=f"comprehensive_video_{lesson_data['order']}",
                file_id=f"file_comprehensive_{lesson_data['order']}",
                cover_url=f"https://via.placeholder.com/640x360/E8F5E8/388E3C?text=全面学医第{lesson_data['order']}课",
                status=VideoStatus.READY
            )
            db.add(lesson)
        
        # 提交所有更改
        db.commit()
        print("成功创建所有课程数据:")
        print(f"   - 基础课程: {basic_course.id}")
        print(f"   - 逐病精讲-失眠调理专题: {insomnia_course.id}")
        print(f"   - 逐病精讲-胃病调理专题: {gastric_course.id}") 
        print(f"   - 全面学医系列: {comprehensive_course.id}")
        
    except Exception as e:
        print(f"创建数据失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    recreate_database()