from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import User
from django.core.validators import (
    # RegexValidator,
    FileExtensionValidator
)
from django.utils import timezone
from django.conf import settings
import os

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
    

# informa/models.py 末尾追加
class WeatherApiQuota(models.Model):
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    used = models.PositiveIntegerField(default=0)
    limit = models.PositiveIntegerField(default=1000)  # 每月上限

    class Meta:
        unique_together = ('year', 'month')
        verbose_name = '天气 API 月度配额'

    def __str__(self):
        return f"{self.year}-{self.month:02d}: {self.used}/{self.limit}"
    
class DeletedMedia(models.Model):
    file_path = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @classmethod
    def clean_expired(cls, days=30):
        expiration_date = timezone.now() - timezone.timedelta(days=days)
        expired_objects = cls.objects.filter(deleted_at__lte=expiration_date)
        for obj in expired_objects:
            if os.path.exists(obj.file_path):
                os.remove(obj.file_path)
        expired_objects.delete()