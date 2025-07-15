from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import (
   WeatherCache, ImageUpload,
)
from .serializers import (
   WeatherCacheSerializer,
   ImageUploadSerializer
)
from django.contrib.auth import get_user_model
from .weather_service import fetch_weather_data
from django.conf import settings
from datetime import timedelta

User = get_user_model()

class WeatherCacheViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]  # 公开
    authentication_classes = []                  # 不需要 JWT
    """
    天气缓存API端点
    
    存储和获取天气数据缓存，按位置(location)唯一索引
    """
    queryset = WeatherCache.objects.all()
    serializer_class = WeatherCacheSerializer
    lookup_field = 'location'  # 使用location作为查找字段
    permission_classes = [permissions.AllowAny]  # 允许公开访问
    
    def get_object(self):
        """重写以支持通过location获取对象"""
        location = self.kwargs['location']
        return get_object_or_404(WeatherCache, location=location)
    
    @action(detail=False, methods=['get'])
    def get_by_location(self, request):
        location = request.query_params.get('location')
        print(1)
        if not location:
            return Response({'error': 'Missing location'}, status=400)
        
        try:
            # 尝试获取缓存
            cache = WeatherCache.objects.get(location=location)
            
            # 如果缓存过期但存在，后台更新
            if cache.expires_at < timezone.now():
                # 异步更新缓存 (不阻塞用户请求)
                from .tasks import update_weather_cache
                update_weather_cache.delay([location])
                
                # 仍返回过期数据（根据需求可改为返回错误）
                serializer = self.get_serializer(cache)
                return Response({
                    **serializer.data,
                    'warning': 'Cache updating in background'
                })
            
            # 返回有效缓存
            serializer = self.get_serializer(cache)
            return Response(serializer.data)
            
        except WeatherCache.DoesNotExist:
            # 首次请求时同步创建缓存
            weather_data = fetch_weather_data(location)
            if 'error' in weather_data:
                return Response(weather_data, status=503)
                
            cache = WeatherCache.objects.create(
                location=location,
                data=weather_data,
                expires_at=timezone.now() + timedelta(
                    hours=settings.CACHE_EXPIRY_HOURS
                )
            )
            serializer = self.get_serializer(cache)
            return Response(serializer.data, status=201)

class ImageUploadViewSet(viewsets.ModelViewSet):
    """
    图片上传API端点
    
    支持用户上传图片，自动记录上传者和上传时间
    """
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = [permissions.IsAuthenticated]  # 需要登录
    
    def perform_create(self, serializer):
        """创建时自动设置上传者为当前用户"""
        serializer.save(uploaded_by=self.request.user)
    
    def get_queryset(self):
        """用户只能看到自己上传的图片（管理员可查看所有）"""
        if self.request.user.is_staff:
            return ImageUpload.objects.all()
        return ImageUpload.objects.filter(uploaded_by=self.request.user)