#!/usr/bin/env python3
"""
自动检测视频文件变化并更新课时记录
"""

import os
import glob
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.database import SessionLocal
from app.models.course import Course, Lesson

class VideoFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_update = time.time()
        
    def on_created(self, event):
        if not event.is_directory and self.is_video_file(event.src_path):
            print(f"检测到新视频文件: {event.src_path}")
            # 等待文件完全上传完成
            time.sleep(2)
            self.update_lessons()
    
    def on_modified(self, event):
        if not event.is_directory and self.is_video_file(event.src_path):
            # 防止频繁触发
            current_time = time.time()
            if current_time - self.last_update > 5:  # 5秒内只更新一次
                print(f"检测到视频文件变化: {event.src_path}")
                time.sleep(1)
                self.update_lessons()
                self.last_update = current_time
    
    def is_video_file(self, filepath):
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        return any(filepath.lower().endswith(ext) for ext in video_extensions)
    
    def update_lessons(self):
        """更新课时的视频文件"""
        try:
            db = SessionLocal()
            
            # 获取所有上传的视频文件
            video_files = []
            video_patterns = [
                'uploads/videos/**/*.mp4',
                'uploads/videos/**/*.avi', 
                'uploads/videos/**/*.mov',
                'uploads/videos/**/*.mkv',
                'uploads/videos/**/*.webm'
            ]
            
            for pattern in video_patterns:
                video_files.extend(glob.glob(pattern, recursive=True))
            
            # 按文件修改时间排序，最新的在前面
            video_files.sort(key=os.path.getmtime, reverse=True)
            
            print(f"找到 {len(video_files)} 个视频文件")
            
            if not video_files:
                print("没有找到视频文件")
                return
                
            # 获取所有课时
            lessons = db.query(Lesson).order_by(Lesson.id).all()
            print(f"找到 {len(lessons)} 个课时记录")
            
            if not lessons:
                print("没有找到课时记录")
                return
                
            # 更新课时的视频URL
            updated_count = 0
            for i, lesson in enumerate(lessons):
                if i < len(video_files):
                    # 使用对应的视频文件
                    video_path = video_files[i]
                    # 转换为Web访问路径
                    web_path = f"/{video_path.replace(os.sep, '/')}"
                    
                    if lesson.video_url != web_path:
                        old_url = lesson.video_url
                        lesson.video_url = web_path
                        print(f"更新课时 {lesson.id}: {lesson.title}")
                        print(f"  新URL: {web_path}")
                        updated_count += 1
                else:
                    # 如果视频文件不够，使用最新的视频文件
                    if video_files:
                        video_path = video_files[0]
                        web_path = f"/{video_path.replace(os.sep, '/')}"
                        if lesson.video_url != web_path:
                            lesson.video_url = web_path
                            updated_count += 1
            
            db.commit()
            print(f"成功更新了 {updated_count} 个课时的视频URL")
            
        except Exception as e:
            db.rollback()
            print(f"更新失败: {e}")
        finally:
            db.close()

def start_monitoring():
    """启动视频文件监控"""
    video_dir = "uploads/videos"
    if not os.path.exists(video_dir):
        print(f"视频目录不存在: {video_dir}")
        return
    
    event_handler = VideoFileHandler()
    observer = Observer()
    observer.schedule(event_handler, video_dir, recursive=True)
    
    print(f"开始监控视频目录: {video_dir}")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n停止监控")
    
    observer.join()

if __name__ == "__main__":
    start_monitoring()