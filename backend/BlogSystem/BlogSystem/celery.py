# yourproject/celery.py
import os
from celery import Celery

# 设置默认的 Django 设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogSystem.settings')

app = Celery('BlogSystem')

# 使用 Django 的设置文件配置 Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 从所有已注册的 Django app 中加载任务
app.autodiscover_tasks()