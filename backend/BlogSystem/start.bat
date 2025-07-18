@echo off
chcp 65001 > nul
title BlogSystem 一键启动

:: 1. 关键路径（全部用引号包住）
set "REDIS_EXE=D:\Software\Redis-x64-5.0.14.1\redis-server.exe"
set "PROJECT_DIR=%~dp0"
set "VENV_PYTHON=E:\项目\个人博客开发\backend\.venv\Scripts\python.exe"

:: 2. 切到项目目录
cd /d "%PROJECT_DIR%"

:: 3. 日志目录
if not exist "logs" mkdir "logs"

:: 4. 启动 Redis
tasklist /FI "IMAGENAME eq redis-server.exe" | find /I "redis-server.exe" > nul
if errorlevel 1 (
    echo [BlogSystem] 启动 Redis ...
    start /B "" "%REDIS_EXE%" > "%PROJECT_DIR%logs\redis.log" 2>&1
    timeout /t 2 > nul
) else (
    echo [BlogSystem] Redis 已在运行
)

:: 5. Celery Worker
echo [BlogSystem] 启动 Celery Worker ...
start /B "" "%VENV_PYTHON%" -m celery -A BlogSystem worker -l info -P gevent ^
    > "%PROJECT_DIR%logs\celery_worker.log" 2>&1

:: 6. Celery Beat
echo [BlogSystem] 启动 Celery Beat ...
start /B "" "%VENV_PYTHON%" -m celery -A BlogSystem beat -l info ^
    > "%PROJECT_DIR%logs\celery_beat.log" 2>&1

:: 7. Django
echo [BlogSystem] 启动 Django ...
start /B "" "%VENV_PYTHON%" manage.py runserver 0.0.0.0:8000 ^
    > "%PROJECT_DIR%logs\django.log" 2>&1

echo.
echo [BlogSystem] 所有服务已后台启动！
echo        日志目录: "%PROJECT_DIR%logs"
echo        浏览器访问: http://127.0.0.1:8000
pause