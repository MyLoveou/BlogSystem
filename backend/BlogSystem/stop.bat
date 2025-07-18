@echo off
chcp 65001
title BlogSystem 一键关闭
taskkill /F /IM redis-server.exe 2>nul
taskkill /F /IM celery.exe       2>nul
taskkill /F /IM python.exe       2>nul
echo [BlogSystem] 已清理所有相关进程
pause
