from django.db import models
# 站点配置模型
class SiteConfig(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.key

# 导航菜单模型
class NavMenu(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "导航菜单"
        verbose_name_plural = "导航菜单"
        
    def __str__(self):
        return self.name