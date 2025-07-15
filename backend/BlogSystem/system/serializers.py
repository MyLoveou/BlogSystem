from rest_framework import serializers
from .models import SiteConfig, NavMenu
from django.contrib.auth import authenticate

class SiteConfigSerializer(serializers.ModelSerializer):
    """站点配置序列化器"""
    class Meta:
        model = SiteConfig
        fields = ['key', 'value', 'updated_at']
        read_only_fields = ['updated_at']  # 自动更新的字段设为只读
        
        # 额外验证：确保key的唯一性
        extra_kwargs = {
            'key': {'validators': []}  # 禁用DRF的默认唯一验证
        }
    
    def validate_key(self, value):
        """自定义key字段验证"""
        # 检查key是否已存在（创建时）
        if self.instance is None and SiteConfig.objects.filter(key=value).exists():
            raise serializers.ValidationError("该配置键已存在")
        # 更新时检查是否被其他实例使用
        if self.instance and SiteConfig.objects.filter(key=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("该配置键已被其他配置使用")
        return value

class NavMenuSerializer(serializers.ModelSerializer):
    """导航菜单序列化器"""
    class Meta:
        model = NavMenu
        fields = '__all__'  # 包含所有字段
        read_only_fields = ['id']  # ID自动生成，设为只读
        
    def validate(self, data):
        """菜单顺序验证"""
        # 确保同一菜单项的order值不重复
        if 'order' in data:
            existing = NavMenu.objects.filter(order=data['order'])
            if self.instance:  # 更新操作
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError(
                    {'order': '该顺序值已被其他菜单项使用'}
                )
        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['username'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError('用户名或密码错误')
        attrs['user'] = user
        return attrs