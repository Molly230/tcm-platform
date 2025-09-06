#!/usr/bin/env python3
"""
使用真实上传的视频文件更新课时数据
"""

import os
import glob
from app.database import SessionLocal
from app.models.course import Course, Lesson

def update_lessons_with_real_videos():
    db = SessionLocal()
    try:
        # 获取所有上传的视频文件
        video_files = []
        
        # 查找所有视频文件
        video_patterns = [
            'uploads/videos/**/*.mp4',
            'uploads/videos/**/*.avi', 
            'uploads/videos/**/*.mov',
            'uploads/videos/**/*.mkv',
            'uploads/videos/**/*.webm'
        ]
        
        for pattern in video_patterns:
            video_files.extend(glob.glob(pattern, recursive=True))
        
        # 按文件修改时间排序，最新的文件在前面
        video_files.sort(key=os.path.getmtime, reverse=True)
        
        print(f"找到 {len(video_files)} 个上传的视频文件:")
        for i, video in enumerate(video_files[:10]):  # 只显示前10个
            print(f"  {i+1}. {video}")
        if len(video_files) > 10:
            print(f"  ... 还有 {len(video_files)-10} 个文件")
        
        if not video_files:
            print("没有找到上传的视频文件")
            return
            
        # 获取所有课时
        lessons = db.query(Lesson).all()
        print(f"\n找到 {len(lessons)} 个课时记录")
        
        if not lessons:
            print("没有找到课时记录")
            return
            
        # 更新课时的视频URL
        updated_count = 0
        for i, lesson in enumerate(lessons):
            if i < len(video_files):
                # 使用相应的真实视频文件
                video_path = video_files[i]
                # 转换为Web访问路径
                web_path = f"/{video_path.replace(os.sep, '/')}"
                
                old_url = lesson.video_url
                lesson.video_url = web_path
                
                print(f"更新课时 {lesson.id}: {lesson.title}")
                print(f"  旧URL: {old_url}")
                print(f"  新URL: {web_path}")
                
                updated_count += 1
            else:
                # 如果视频文件不够，使用第一个视频文件
                if video_files:
                    video_path = video_files[0]
                    web_path = f"/{video_path.replace(os.sep, '/')}"
                    lesson.video_url = web_path
                    updated_count += 1
        
        db.commit()
        print(f"\n成功更新了 {updated_count} 个课时的视频URL")
        
        # 验证更新结果
        print("\n验证更新结果:")
        sample_lessons = db.query(Lesson).limit(5).all()
        for lesson in sample_lessons:
            print(f"课时 {lesson.id}: {lesson.title}")
            print(f"  视频URL: {lesson.video_url}")
            
    except Exception as e:
        db.rollback()
        print(f"更新失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_lessons_with_real_videos()