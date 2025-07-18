from rest_framework import serializers
from.models import Article, Category, Tag, Page, FriendLink

from django.utils import timezone
from django.utils.text import slugify

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """用户模型序列化器 (用于关联字段展示)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = fields  # 所有字段只读


class CategoryTreeSerializer(serializers.ModelSerializer):
    """分类树形结构序列化器（用于嵌套）"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']

class CategorySerializer(serializers.ModelSerializer):
    """分类模型序列化器"""
    # 嵌套展示父级分类信息
    parent = CategoryTreeSerializer(read_only=True)
    
    # 父级分类ID（用于创建/更新）
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='parent',
        write_only=True,
        allow_null=True,
        required=False
    )
    
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """创建时自动生成slug"""
        instance = super().create(validated_data)
        if not instance.slug:
            instance.slug = slugify(instance.name)
            instance.save()
        return instance
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("名称不能为空")
        return value

class TagSerializer(serializers.ModelSerializer):
    """标签模型序列化器"""
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'created_at', 'usage_count']
        
    def validate_color(self, value):
        """验证颜色格式"""
        import re
        if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
            raise serializers.ValidationError("颜色格式必须为#RGB或#RRGGBB")
        return value
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("名称不能为空")
        return value

class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表序列化器（简化版）"""
    author = serializers.CharField(source='author.username', read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    primary_category = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'excerpt', 'author', 'status', 'review_status',
            'cover_image_url', 'primary_category', 'published_at', 'views_count'
        ]
        read_only_fields = fields
    
    def get_cover_image_url(self, obj):
        """安全获取封面图URL"""
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None
    
    def get_primary_category(self, obj):
        """获取第一个分类名称"""
        if obj.categories.exists():
            return obj.categories.first().name
        return None

class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器（完整版）"""
    author = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    categories = CategoryTreeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    
    # 用于接收分类和标签ID列表
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='categories',
        many=True,
        write_only=True
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        write_only=True
    )
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'html_content', 'excerpt', 'author',
            'categories', 'tags', 'status', 'review_status', 'reviewer',
            'cover_image', 'cover_image_url', 'slug', 'created_at', 'updated_at',
            'published_at', 'views_count', 'is_deleted', 'deleted_at',
            'category_ids', 'tag_ids'
        ]
        read_only_fields = [
            'id', 'slug', 'created_at', 'updated_at', 'published_at', 
            'views_count', 'cover_image_url', 'html_content', 'is_deleted', 
            'deleted_at'
        ]
    
    def get_cover_image_url(self, obj):
        """安全获取封面图URL"""
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None
    
    def validate(self, data):
        """自定义验证逻辑"""
        # 状态为发布时必须有发布时间
        if data.get('status') == 'published':
            if not data.get('published_at') and not self.instance.published_at:
                data['published_at'] = timezone.now()
        
        # 审核通过时需要设置审核人
        if data.get('review_status') == 'approved':
            if not data.get('reviewer') and self.context.get('request'):
                data['reviewer'] = self.context['request'].user
        
        return data
    
    def create(self, validated_data):
        """创建文章时自动设置作者"""
        # 从请求上下文中获取当前用户
        if self.context.get('request'):
            validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("标题不能为空")
        return value


class PageSerializer(serializers.ModelSerializer):
    """页面模型序列化器"""
    class Meta:
        model = Page
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        
        # 额外验证配置
        extra_kwargs = {
            'page_type': {'validators': []}  # 禁用默认唯一性验证
        }
    
    def validate_page_type(self, value):
        """验证页面类型唯一性"""
        # 创建时检查
        if self.instance is None and Page.objects.filter(page_type=value).exists():
            raise serializers.ValidationError("该页面类型已存在")
        # 更新时检查
        if self.instance and Page.objects.filter(page_type=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("该页面类型已被其他页面使用")
        return value

class FriendLinkSerializer(serializers.ModelSerializer):
    """友情链接序列化器"""
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FriendLink
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'logo_url']
    
    def get_logo_url(self, obj):
        """安全获取Logo URL"""
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None