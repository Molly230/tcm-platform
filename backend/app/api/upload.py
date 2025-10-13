"""
文件上传API路由
"""
import os
import uuid
import shutil
import magic
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.core.permissions import require_admin_role
from app import models

router = APIRouter(tags=["upload"])

# 上传文件配置
UPLOAD_DIRECTORY = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {
    "image": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "video": [".mp4", ".avi", ".mov", ".wmv", ".flv"],
    "document": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls"]
}

# MIME类型白名单
ALLOWED_MIME_TYPES = {
    "image": [
        "image/jpeg", "image/png", "image/gif", 
        "image/webp", "image/bmp", "image/tiff"
    ],
    "video": [
        "video/mp4", "video/avi", "video/quicktime", 
        "video/x-msvideo", "video/x-flv"
    ],
    "document": [
        "application/pdf", "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain", "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ]
}

# 危险文件扩展名黑名单
DANGEROUS_EXTENSIONS = {
    ".exe", ".bat", ".cmd", ".com", ".pif", ".scr", ".vbs", 
    ".js", ".jar", ".sh", ".php", ".asp", ".aspx", ".jsp", 
    ".py", ".pl", ".cgi", ".htaccess", ".htpasswd"
}

class UploadResponse(BaseModel):
    success: bool
    message: str
    file_url: Optional[str] = None
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None

def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return Path(filename).suffix.lower()

def is_safe_filename(filename: str) -> bool:
    """检查文件名是否安全"""
    # 检查危险扩展名
    ext = get_file_extension(filename)
    if ext in DANGEROUS_EXTENSIONS:
        return False
    
    # 检查文件名中的危险字符
    dangerous_chars = ["<", ">", ":", "\"", "|", "?", "*", "\0"]
    for char in dangerous_chars:
        if char in filename:
            return False
    
    # 检查路径遍历攻击
    if ".." in filename or "/" in filename or "\\" in filename:
        return False
    
    return True


def validate_mime_type(content: bytes, file_type: str) -> bool:
    """验证文件的真实MIME类型"""
    try:
        # 使用python-magic检测真实MIME类型
        mime_type = magic.from_buffer(content, mime=True)
        
        # 对于图片类型，添加更宽松的检查
        if file_type == "image":
            # 检查文件签名
            if content.startswith(b'\x89PNG\r\n\x1a\n'):
                return True  # PNG格式
            if content.startswith(b'\xff\xd8\xff'):
                return True  # JPEG格式
            # 检查MIME类型
            if mime_type in ALLOWED_MIME_TYPES["image"]:
                return True
            # 额外的MIME类型支持
            if mime_type in ["image/jpg", "image/pjpeg"]:
                return True
        
        if file_type in ALLOWED_MIME_TYPES:
            return mime_type in ALLOWED_MIME_TYPES[file_type]
        
        # 检查所有允许的MIME类型
        all_mime_types = []
        for mime_types in ALLOWED_MIME_TYPES.values():
            all_mime_types.extend(mime_types)
        
        return mime_type in all_mime_types
    except Exception as e:
        # 如果无法检测MIME类型，对于图片类型使用文件扩展名验证
        if file_type == "image":
            return True  # 允许通过扩展名验证
        return False


def scan_for_malware(content: bytes) -> bool:
    """简单的恶意文件扫描"""
    # 检查常见的恶意文件签名
    malware_signatures = [
        b"MZ",  # PE executable
        b"<?php",  # PHP code
        b"<script",  # JavaScript
        b"javascript:",  # JavaScript URL
        b"eval(",  # JavaScript eval
        b"exec(",  # Code execution
        b"system(",  # System command
    ]
    
    content_lower = content.lower()
    for signature in malware_signatures:
        if signature.lower() in content_lower:
            return False
    
    return True


def calculate_file_hash(content: bytes) -> str:
    """计算文件哈希值"""
    return hashlib.sha256(content).hexdigest()


def is_allowed_file(filename: str, file_type: str = None) -> bool:
    """检查文件类型是否允许"""
    # 首先检查文件名安全性
    if not is_safe_filename(filename):
        return False
    
    ext = get_file_extension(filename)
    
    if file_type and file_type in ALLOWED_EXTENSIONS:
        return ext in ALLOWED_EXTENSIONS[file_type]
    
    # 检查所有允许的扩展名
    all_extensions = []
    for extensions in ALLOWED_EXTENSIONS.values():
        all_extensions.extend(extensions)
    
    return ext in all_extensions

def generate_filename(original_filename: str) -> str:
    """生成唯一文件名"""
    ext = get_file_extension(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}{ext}"

@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...), 
    file_type: Optional[str] = None,
    current_user: models.User = Depends(require_admin_role)
):
    """
    上传单个文件
    
    Args:
        file: 上传的文件
        file_type: 文件类型限制 (image, video, document)
    """
    try:
        # 检查文件是否为空
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="未选择文件"
            )
        
        # 检查文件大小
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"文件大小超过限制 ({MAX_FILE_SIZE // (1024*1024)}MB)"
            )
        
        # 检查文件类型
        if not is_allowed_file(file.filename, file_type):
            allowed_types = ALLOWED_EXTENSIONS.get(file_type, "支持的格式")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件类型，{allowed_types}"
            )
        
        # 验证MIME类型
        if not validate_mime_type(content, file_type or ""):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件内容与扩展名不匹配"
            )
        
        # 恶意文件扫描
        if not scan_for_malware(content):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="检测到潜在恶意文件，上传被拒绝"
            )
        
        # 确定上传目录
        if file_type == "image":
            upload_dir = Path(UPLOAD_DIRECTORY) / "images"
        elif file_type == "video":
            upload_dir = Path(UPLOAD_DIRECTORY) / "videos"
        elif file_type == "document":
            upload_dir = Path(UPLOAD_DIRECTORY) / "documents"
        else:
            upload_dir = Path(UPLOAD_DIRECTORY) / "general"
        
        # 创建上传目录
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成唯一文件名
        new_filename = generate_filename(file.filename)
        file_path = upload_dir / new_filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # 生成访问URL
        relative_path = str(file_path).replace("\\", "/")
        file_url = f"/uploads/{relative_path.split('uploads/')[-1]}"
        
        return UploadResponse(
            success=True,
            message="文件上传成功",
            file_url=file_url,
            file_path=str(file_path),
            file_name=new_filename,
            file_size=len(content)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败: {str(e)}"
        )

@router.post("/upload/multiple", response_model=List[UploadResponse])
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    file_type: Optional[str] = None,
    current_user: models.User = Depends(require_admin_role)
):
    """
    上传多个文件
    
    Args:
        files: 上传的文件列表
        file_type: 文件类型限制 (image, video, document)
    """
    if len(files) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="一次最多上传10个文件"
        )
    
    results = []
    for file in files:
        try:
            result = await upload_file(file, file_type)
            results.append(result)
        except HTTPException as e:
            results.append(UploadResponse(
                success=False,
                message=f"文件 {file.filename} 上传失败: {e.detail}",
                file_name=file.filename
            ))
    
    return results

@router.post("/upload/image", response_model=UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(require_admin_role)
):
    """上传图片文件"""
    return await upload_file(file, "image")

@router.post("/upload/video", response_model=UploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    current_user: models.User = Depends(require_admin_role)
):
    """上传视频文件"""
    return await upload_file(file, "video")

@router.delete("/upload/{file_path:path}")
async def delete_file(
    file_path: str,
    current_user: models.User = Depends(require_admin_role)
):
    """
    删除已上传的文件
    
    Args:
        file_path: 文件路径（相对于uploads目录）
    """
    try:
        full_path = Path(UPLOAD_DIRECTORY) / file_path
        
        # 检查文件是否存在
        if not full_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
        
        # 安全检查：确保文件在uploads目录内
        if not str(full_path.resolve()).startswith(str(Path(UPLOAD_DIRECTORY).resolve())):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的文件路径"
            )
        
        # 删除文件
        full_path.unlink()
        
        return {"success": True, "message": "文件删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件删除失败: {str(e)}"
        )

@router.get("/upload/info/{file_path:path}")
async def get_file_info(file_path: str):
    """
    获取文件信息
    
    Args:
        file_path: 文件路径（相对于uploads目录）
    """
    try:
        full_path = Path(UPLOAD_DIRECTORY) / file_path
        
        # 检查文件是否存在
        if not full_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
        
        stat = full_path.stat()
        
        return {
            "filename": full_path.name,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "url": f"/uploads/{file_path}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取文件信息失败: {str(e)}"
        )