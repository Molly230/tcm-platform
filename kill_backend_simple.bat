@echo off
echo ============================================================
echo 终止占用8001端口的进程
echo ============================================================
echo.

REM 查找占用8001端口的进程PID
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001.*LISTENING') do (
    echo 找到进程 PID: %%a
    taskkill /F /PID %%a 2>nul
    if errorlevel 1 (
        echo   失败: 无法终止进程 %%a
    ) else (
        echo   成功: 已终止进程 %%a
    )
)

echo.
echo ============================================================
echo 检查是否还有进程占用8001端口
echo ============================================================
netstat -ano | findstr :8001

echo.
echo 完成！如果上面没有输出，说明端口已释放。
pause
