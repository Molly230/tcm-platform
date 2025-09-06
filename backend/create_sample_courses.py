#!/usr/bin/env python3
"""
创建示例课程数据
"""

from app.database import SessionLocal
from app.models.course import Course, CourseCategory
from app.models.user import User

def create_sample_courses():
    db = SessionLocal()
    try:
        # 检查是否已有课程数据
        existing_courses = db.query(Course).count()
        if existing_courses > 0:
            print(f"已存在 {existing_courses} 个课程，跳过创建")
            return

        # 创建示例课程数据
        sample_courses = [
            # 中医基础课程
            {
                "title": "中医基础理论入门",
                "description": "从阴阳五行学说开始，系统讲解中医基础理论知识",
                "category": CourseCategory.BASIC,
                "instructor": "张教授",
                "price": 299.0,
                "is_free": False,
                "is_published": True,
                "total_lessons": 12,
                "total_duration": 720,
                "duration": "12课时"
            },
            {
                "title": "经络穴位详解",
                "description": "详细讲解人体经络穴位分布与作用机理",
                "category": CourseCategory.BASIC,
                "instructor": "李医师",
                "price": 399.0,
                "is_free": False,
                "is_published": True,
                "total_lessons": 16,
                "total_duration": 960,
                "duration": "16课时"
            },
            
            # 四季养生课程
            {
                "title": "春季养生之道",
                "description": "春季如何顺应自然规律，调养身体健康",
                "category": CourseCategory.SEASONAL,
                "instructor": "王养生师",
                "price": 0,
                "is_free": True,
                "is_published": True,
                "total_lessons": 6,
                "total_duration": 360,
                "duration": "6课时"
            },
            {
                "title": "四季养生全攻略",
                "description": "一年四季的养生方法与注意事项",
                "category": CourseCategory.SEASONAL,
                "instructor": "王养生师",
                "price": 199.0,
                "is_free": False,
                "is_published": True,
                "total_lessons": 24,
                "total_duration": 1440,
                "duration": "24课时"
            },
            
            # 药膳食疗课程
            {
                "title": "家常药膳制作",
                "description": "学习制作日常保健药膳，食药同源养生法",
                "category": CourseCategory.DIET,
                "instructor": "陈药膳师",
                "price": 299.0,
                "is_free": False,
                "is_published": True,
                "total_lessons": 15,
                "total_duration": 900,
                "duration": "15课时"
            },
            {
                "title": "药膳食疗基础",
                "description": "了解食物的药性，掌握食疗基本原理",
                "category": CourseCategory.DIET,
                "instructor": "陈药膳师",
                "price": 0,
                "is_free": True,
                "is_published": True,
                "total_lessons": 8,
                "total_duration": 480,
                "duration": "8课时"
            },
            
            # 推拿按摩课程
            {
                "title": "家庭推拿按摩技法",
                "description": "学习简单实用的家庭推拿按摩手法",
                "category": CourseCategory.MASSAGE,
                "instructor": "刘推拿师",
                "price": 399.0,
                "is_free": False,
                "is_published": True,
                "total_lessons": 20,
                "total_duration": 1200,
                "duration": "20课时"
            },
            
            # 本草方剂课程
            {
                "title": "常用中药材识别",
                "description": "认识常见中药材的性味归经与功效",
                "category": CourseCategory.HERB,
                "instructor": "孙药师",
                "price": 499.0,
                "is_free": False,
                "is_published": True,
                "total_lessons": 30,
                "total_duration": 1800,
                "duration": "30课时"
            },
            {
                "title": "经典方剂解析",
                "description": "深入解析中医经典方剂的配伍规律",
                "category": CourseCategory.HERB,
                "instructor": "孙药师",
                "price": 0,
                "is_free": True,
                "is_published": True,
                "total_lessons": 10,
                "total_duration": 600,
                "duration": "10课时"
            },
            
            # 逐病精讲课程
            {
                "title": "失眠症中医诊治",
                "description": "深入讲解失眠的中医病因病机与治疗方案",
                "category": CourseCategory.DISEASE_FOCUSED,
                "instructor": "马主任医师",
                "price": 599.0,
                "is_free": False,
                "is_published": True,
                "total_lessons": 18,
                "total_duration": 1080,
                "duration": "18课时"
            },
            {
                "title": "高血压中医调理",
                "description": "高血压的中医辨证论治与生活调理",
                "category": CourseCategory.DISEASE_FOCUSED,
                "instructor": "马主任医师",
                "price": 599.0,
                "is_free": False,
                "is_published": True,
                "total_lessons": 22,
                "total_duration": 1320,
                "duration": "22课时"
            },
            
            # 全面学医课程
            {
                "title": "中医临床思维培养",
                "description": "系统培养中医临床诊治思维，从理论到实践",
                "category": CourseCategory.COMPREHENSIVE,
                "instructor": "赵名医",
                "price": 1999.0,
                "is_free": False,
                "is_published": True,
                "total_lessons": 60,
                "total_duration": 3600,
                "duration": "60课时"
            },
            {
                "title": "中医入门体验课",
                "description": "零基础学中医，体验中医诊疗的神奇魅力",
                "category": CourseCategory.COMPREHENSIVE,
                "instructor": "赵名医",
                "price": 0,
                "is_free": True,
                "is_published": True,
                "total_lessons": 5,
                "total_duration": 300,
                "duration": "5课时"
            }
        ]

        # 插入课程数据
        for course_data in sample_courses:
            course = Course(**course_data)
            db.add(course)

        db.commit()
        print(f"成功创建了 {len(sample_courses)} 个示例课程！")
        
        # 显示创建的课程
        for course in db.query(Course).all():
            print(f"- {course.title} ({course.category}) - {'免费' if course.is_free else f'¥{course.price}'}")

    except Exception as e:
        db.rollback()
        print(f"创建课程失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_courses()