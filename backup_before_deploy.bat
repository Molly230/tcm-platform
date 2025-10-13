@echo off
chcp 65001 >nul
echo ========================================
echo   阿里云部署前备份脚本
echo ========================================
echo.

:: 创建备份目录
set BACKUP_DIR=deployment_backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%
mkdir "%BACKUP_DIR%" 2>nul

echo [1/5] 备份SQLite数据库...
copy backend\tcm_backend.db "%BACKUP_DIR%\tcm_backend.db" >nul
if exist backend\tcm_backend.db.backup* (
    xcopy /E /I /Q backend\tcm_backend.db.backup* "%BACKUP_DIR%\db_backups\" >nul
)
echo ✅ 数据库备份完成

echo.
echo [2/5] 备份上传文件...
if exist backend\uploads (
    xcopy /E /I /Q backend\uploads "%BACKUP_DIR%\uploads\" >nul
    echo ✅ 上传文件备份完成
) else (
    echo ⚠️  未找到uploads目录
)

echo.
echo [3/5] 备份配置文件...
copy backend\.env "%BACKUP_DIR%\.env.backup" >nul
copy frontend\.env.production "%BACKUP_DIR%\.env.frontend.backup" 2>nul
if exist backend\cert (
    xcopy /E /I /Q backend\cert "%BACKUP_DIR%\cert\" >nul
)
echo ✅ 配置文件备份完成

echo.
echo [4/5] 生成强随机SECRET_KEY...
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" > "%BACKUP_DIR%\new_secret_key.txt"
echo ✅ 新密钥已保存到: %BACKUP_DIR%\new_secret_key.txt

echo.
echo [5/5] 生成PostgreSQL密码...
python -c "import secrets, string; chars = string.ascii_letters + string.digits + '!@#$%%'; print('PostgreSQL密码: ' + ''.join(secrets.choice(chars) for _ in range(20)))" > "%BACKUP_DIR%\postgres_password.txt"
echo ✅ 数据库密码已保存到: %BACKUP_DIR%\postgres_password.txt

echo.
echo ========================================
echo   备份完成！
echo ========================================
echo 备份位置: %cd%\%BACKUP_DIR%
echo.
echo 📋 备份内容：
dir /B "%BACKUP_DIR%"
echo.
echo ⚠️  请妥善保管备份文件，特别是：
echo    - new_secret_key.txt （SECRET_KEY）
echo    - postgres_password.txt （数据库密码）
echo    - .env.backup （原始配置）
echo.
echo 按任意键打开备份目录...
pause >nul
explorer "%BACKUP_DIR%"
