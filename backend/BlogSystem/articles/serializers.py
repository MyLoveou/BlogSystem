from rest_framework import serializers

from.models import Article, Category, Tag, Page, FriendLink
from informa.models import ImageUpload
from django.utils import timezone
from django.utils.text import slugify

from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """用户模型序列化器 (用于关联字段展示)"""
    class Meta:
        model = User
        fields = ['id', 'username']
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
    author = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    
    # 输出时嵌套展示
    categories = CategoryTreeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    # 写入时使用这些字段
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )
    tag_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    category_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    # cover_image_id = serializers.PrimaryKeyRelatedField(
    #     queryset=ImageUpload.objects.all(),
    #     write_only=True,
    #     required=False,
    #     help_text='传图片上传表的 ID 作为封面'
    #  )
    cover_image_url = serializers.URLField(
        write_only=True,
        required=False,
        help_text='传图片完整 URL，后端将根据 URL 查找对应 ImageUpload'
    )
    cover_image_url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'html_content', 'excerpt',
            'author', 'categories', 'tags', 'status', 'review_status',
            'reviewer', 'slug', 'cover_image_url',
            'created_at', 'updated_at', 'published_at', 'views_count',
            'is_deleted', 'deleted_at',
            'category_ids', 'tag_ids', 'tag_names', 'category_names',
        ]
        read_only_fields = [
            'id', 'slug', 'created_at', 'updated_at', 'published_at',
            'views_count', 
            'is_deleted', 'deleted_at'
        ]

    def get_cover_image_url(self, obj):
         # 只读方法，拼接完整 URL
         if obj.cover_image and obj.cover_image.image:
             request = self.context.get('request')
             path = obj.cover_image.image.url
             return request.build_absolute_uri(path) if request else path
         return None

    def validate(self, data):
        if data.get('status') == 'published' and not data.get('published_at'):
            data['published_at'] = timezone.now()
        if data.get('review_status') == 'approved' and not data.get('reviewer'):
            data['reviewer'] = self.context.get('request').user
        return data

    def create(self, validated_data):

        # 先剥离所有 M2M 相关字段
        cat_ids = validated_data.pop('category_ids', [])
        tag_ids = validated_data.pop('tag_ids', [])
        cat_names = validated_data.pop('category_names', [])
        tag_names = validated_data.pop('tag_names', [])

        # 创建文章
        article = Article.objects.create(**validated_data)
 
        # 关联已有分类/标签
        if cat_ids:
            article.categories.set(cat_ids)
        if tag_ids:
            article.tags.set(tag_ids)

        # 按名称新建或获取再关联
        for name in cat_names:
            cat, _ = Category.objects.get_or_create(name=name)
            article.categories.add(cat)
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            article.tags.add(tag)

        return article

    def update(self, instance, validated_data):
        # 同样先处理所有写入字段
        cat_ids = validated_data.pop('category_ids', None)
        tag_ids = validated_data.pop('tag_ids', None)
        cat_names = validated_data.pop('category_names', [])
        tag_names = validated_data.pop('tag_names', [])

        # 普通字段更新
        instance = super().update(instance, validated_data)

        # 重新设置分类
        if cat_ids is not None:
            instance.categories.set(cat_ids)
        else:
            # 如果只按名称操作，也可以先清空
            instance.categories.clear()
        for name in cat_names:
            cat, _ = Category.objects.get_or_create(name=name)
            instance.categories.add(cat)

        # 重新设置标签
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        else:
            instance.tags.clear()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            instance.tags.add(tag)


        return instance
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