"""
清理数据库并重新创建测试数据
"""
from app.database import SessionLocal
from app.models.course import Course, Lesson

def clean_and_recreate_data():
    db = SessionLocal()
    
    try:
        # 清理所有课程和课时数据
        print("正在清理旧数据...")
        db.query(Lesson).delete()
        db.query(Course).delete()
        db.commit()
        print("旧数据清理完成")
        
        # 创建新的测试课程
        print("正在创建新测试数据...")
        test_course = Course(
            title="中医养生基础课程",
            description="学习中医养生的基本理论和实践方法",
            category="basic",  # 使用小写，符合枚举值
            instructor="张医师",
            price=99.0,
            is_free=False,
            is_published=True,
            total_lessons=3,
            total_duration=1800  # 30分钟
        )
        
        db.add(test_course)
        db.commit()
        db.refresh(test_course)
        
        # 创建测试视频课时
        lessons = [
            Lesson(
                course_id=test_course.id,
                title="第一课：中医基础理论",
                description="介绍中医的基本理论体系",
                order=1,
                duration=600,  # 10分钟
                video_url="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
                video_id="test_video_1",
                file_id="file_001",
                cover_url="https://via.placeholder.com/640x360/4CAF50/FFFFFF?text=第一课",
                status="ready",
                is_free=True
            ),
            Lesson(
                course_id=test_course.id,
                title="第二课：经络与穴位",
                description="了解人体经络系统和重要穴位",
                order=2,
                duration=600,  # 10分钟
                video_url="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4",
                video_id="test_video_2",
                file_id="file_002", 
                cover_url="https://via.placeholder.com/640x360/2196F3/FFFFFF?text=第二课",
                status="ready",
                is_free=False
            ),
            Lesson(
                course_id=test_course.id,
                title="第三课：养生实践方法",
                description="日常养生的具体方法和注意事项",
                order=3,
                duration=600,  # 10分钟
                video_url="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_5mb.mp4",
                video_id="test_video_3",
                file_id="file_003",
                cover_url="https://via.placeholder.com/640x360/FF9800/FFFFFF?text=第三课",
                status="ready",
                is_free=False
            )
        ]
        
        for lesson in lessons:
            db.add(lesson)
        
        db.commit()
        
        print("测试数据创建成功:")
        print(f"   课程ID: {test_course.id}")
        print(f"   课程标题: {test_course.title}")
        print(f"   课程分类: {test_course.category}")
        print(f"   课时数量: {len(lessons)}")
        print(f"   课程状态: {'已发布' if test_course.is_published else '未发布'}")
        
        for i, lesson in enumerate(lessons, 1):
            print(f"   课时{i}: {lesson.title} ({'免费' if lesson.is_free else '付费'})")
            
        return test_course.id
        
    except Exception as e:
        print(f"操作失败: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    course_id = clean_and_recreate_data()
    if course_id:
        print(f"\n现在可以访问以下URL测试:")
        print(f"   课程列表: http://localhost:3001/courses")
        print(f"   课程详情: http://localhost:3001/courses/{course_id}")
        print(f"   API测试: http://localhost:8000/api/courses/{course_id}")