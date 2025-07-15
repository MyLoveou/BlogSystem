# tasks.py
from celery import shared_task
from .weather_service import update_weather_cache
from django.conf import settings
from django.utils import timezone
from .models import WeatherApiQuota
@shared_task
def update_weather_caches():
    """定时更新天气缓存任务"""
    # 从配置获取需要监控的位置列表
    locations = settings.MONITORED_LOCATIONS  
    # 示例: ['Beijing', 'Shanghai', 'New York']
    
    update_weather_cache(locations)

@shared_task
def reset_monthly_quota():
    """每月 1 号 0 点把计数器归零"""
    today = timezone.now().date()
    WeatherApiQuota.objects.filter(year=today.year, month=today.month).update(used=0)