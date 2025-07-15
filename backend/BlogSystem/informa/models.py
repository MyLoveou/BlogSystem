from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import User
from django.core.validators import (
    # RegexValidator,
    FileExtensionValidator
)

# Create your models here.
# 天气缓存模型
class WeatherCache(models.Model):
    location = models.CharField(max_length=100, unique=True)
    data = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Weather for {self.location}"

# 图片上传模型
class ImageUpload(models.Model):
    id = ShortUUIDField(primary_key=True)
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])]
    )
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='uploaded_images'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image {self.id}"