from rest_framework import serializers
from .models import WeatherCache, ImageUpload

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """用户模型序列化器 (用于关联字段展示)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = fields  # 所有字段只读


class WeatherCacheSerializer(serializers.ModelSerializer):
    """天气缓存序列化器"""
    class Meta:
        model = WeatherCache
        fields = '__all__'
        read_only_fields = ['last_updated']  # 最后更新时间自动设置

class ImageUploadSerializer(serializers.ModelSerializer):
    """图片上传序列化器"""
    # 嵌套展示上传者信息
    uploaded_by = UserSerializer(read_only=True)
    
    # 图片URL字段（自动生成）
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ImageUpload
        fields = ['id', 'image', 'image_url', 'uploaded_by', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'image_url']
        
    def get_image_url(self, obj):
        """生成图片完整URL"""
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None