#!/usr/bin/env python3
"""
为现有课程创建示例课时数据
"""

from app.database import SessionLocal
from app.models.course import Course, Lesson, VideoStatus

def create_sample_lessons():
    db = SessionLocal()
    try:
        # 获取所有课程
        courses = db.query(Course).all()
        if not courses:
            print("没有找到课程数据")
            return

        lesson_count = 0
        
        for course in courses:
            print(f"\n为课程 '{course.title}' 创建课时...")
            
            # 为每个课程创建3-5个课时
            lessons_data = [
                {
                    "title": f"第1课：{course.title}基础入门", 
                    "description": f"介绍{course.title}的基本概念和理论基础",
                    "order": 1,
                    "duration": 900,  # 15分钟
                    "is_free": True  # 第一课免费体验
                },
                {
                    "title": f"第2课：{course.title}核心理论", 
                    "description": f"深入讲解{course.title}的核心理论知识",
                    "order": 2, 
                    "duration": 1200,  # 20分钟
                    "is_free": False
                },
                {
                    "title": f"第3课：{course.title}实践应用", 
                    "description": f"学习{course.title}的实际应用方法和技巧",
                    "order": 3,
                    "duration": 1500,  # 25分钟
                    "is_free": False
                }
            ]
            
            # 根据课程类型添加特色课时
            if course.category.value == "basic":
                lessons_data.append({
                    "title": f"第4课：{course.title}案例分析",
                    "description": f"通过典型案例深入理解{course.title}",
                    "order": 4,
                    "duration": 1800,  # 30分钟
                    "is_free": False
                })
            elif course.category.value == "disease_focused" or course.category == "逐病精讲":
                lessons_data.extend([
                    {
                        "title": f"第4课：病理机制分析",
                        "description": "从中医角度分析疾病的发生发展机制",
                        "order": 4,
                        "duration": 2100,  # 35分钟
                        "is_free": False
                    },
                    {
                        "title": f"第5课：治疗方案设计",
                        "description": "学习制定个体化的中医治疗方案",
                        "order": 5,
                        "duration": 2400,  # 40分钟
                        "is_free": False
                    }
                ])
            elif course.category.value == "comprehensive" or course.category == "全面学医":
                lessons_data.extend([
                    {
                        "title": f"第4课：临床思维训练",
                        "description": "培养中医临床诊断思维能力",
                        "order": 4,
                        "duration": 2700,  # 45分钟
                        "is_free": False
                    },
                    {
                        "title": f"第5课：综合实践演练",
                        "description": "通过综合案例提高实战能力",
                        "order": 5,
                        "duration": 3000,  # 50分钟
                        "is_free": False
                    }
                ])
            
            # 创建课时记录
            for lesson_data in lessons_data:
                lesson = Lesson(
                    course_id=course.id,
                    title=lesson_data["title"],
                    description=lesson_data["description"],
                    order=lesson_data["order"],
                    duration=lesson_data["duration"],
                    # 使用示例视频URL
                    video_url=f"https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_{lesson_data['order']}mb.mp4",
                    video_id=f"sample_video_{course.id}_{lesson_data['order']}",
                    file_id=f"file_{course.id}_{lesson_data['order']:03d}",
                    cover_url=f"https://via.placeholder.com/640x360/4CAF50/FFFFFF?text=第{lesson_data['order']}课",
                    status=VideoStatus.READY,
                    is_free=lesson_data["is_free"],
                    transcript=f"这是{lesson_data['title']}的视频字幕内容..."
                )
                db.add(lesson)
                lesson_count += 1
            
            # 更新课程的课时统计
            course.total_lessons = len(lessons_data)
            course.total_duration = sum(l["duration"] for l in lessons_data)
            
        db.commit()
        print(f"\n成功创建了 {lesson_count} 个课时，覆盖 {len(courses)} 个课程！")
        
        # 显示结果
        print("\n课程和课时概览:")
        for course in db.query(Course).all():
            lessons = db.query(Lesson).filter(Lesson.course_id == course.id).all()
            print(f"📚 {course.title}: {len(lessons)}课时 ({sum(l.duration for l in lessons)//60}分钟)")
            for lesson in lessons[:3]:  # 只显示前3课
                print(f"   - {lesson.title} ({'免费' if lesson.is_free else '付费'})")
            if len(lessons) > 3:
                print(f"   - ... 还有{len(lessons)-3}课时")
        
    except Exception as e:
        db.rollback()
        print(f"创建课时失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_lessons()