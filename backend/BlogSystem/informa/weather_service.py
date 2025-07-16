# weather_service.py
import requests
from django.utils import timezone
from .models import WeatherCache
from django.conf import settings
from datetime import timedelta
# import calendar
from datetime import date
from django.db import transaction
from .models import WeatherApiQuota
# 配置示例 (settings.py)
# WEATHER_API_KEY = "your_api_key"
# WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"
# CACHE_EXPIRY_HOURS = 1  # 缓存有效期(小时)

def fetch_weather_data(location: str) -> dict:
    if not can_call_weather_api(limit=1000):
        return {'error': '本月天气 API 配额已用完'}

    params = {
        'key': settings.WEATHER_API_KEY,
        'location': location,
    }
    try:
        resp = requests.get(settings.WEATHER_API_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def update_weather_cache(locations: list):
    """更新或创建天气缓存记录"""
    for location in locations:
        # 检查是否存在有效缓存
        cache, created = WeatherCache.objects.get_or_create(
            location=location,
            defaults={'data': {}, 'expires_at': timezone.now()}
        )
        
        # 仅当缓存不存在或已过期时更新
        if created or cache.expires_at < timezone.now():
            weather_data = fetch_weather_data(location)
            
            if 'error' not in weather_data:
                # 更新缓存数据和过期时间
                cache.data = weather_data
                cache.expires_at = timezone.now() + timedelta(
                    hours=settings.CACHE_EXPIRY_HOURS
                )
                cache.save()

def can_call_weather_api(limit=1000) -> bool:
    """
    判断本月是否还能再调天气 API
    若可以，则自动把计数器 +1
    """
    today = date.today()
    quota, created = WeatherApiQuota.objects.get_or_create(
        year=today.year,
        month=today.month,
        defaults={'limit': limit}
    )

    if quota.used >= quota.limit:
        return False

    with transaction.atomic():
        # 行级锁，防止并发超卖
        quota.refresh_from_db()
        if quota.used < quota.limit:
            quota.used += 1
            quota.save()
            return True
    return False