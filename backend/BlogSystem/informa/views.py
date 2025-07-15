from rest_framework import viewsets, permissions, status
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
        """通过位置获取天气缓存"""
        location = request.query_params.get('location')
        if not location:
            return Response({'error': '缺少location参数'}, status=status.HTTP_400_BAD_REQUEST)
        
        cache = WeatherCache.objects.filter(location=location).first()
        if not cache:
            return Response({'error': '未找到天气缓存'}, status=status.HTTP_404_NOT_FOUND)
        
        # 检查缓存是否过期
        if cache.expires_at < timezone.now():
            cache.delete()  # 删除过期缓存
            return Response({'error': '缓存已过期'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(cache)
        return Response(serializer.data)

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