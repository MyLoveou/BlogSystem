from django.db import models
from shortuuidfield import ShortUUIDField
from django.utils.text import slugify
from django.urls import reverse

# from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator, FileExtensionValidator
from django.conf import settings
from .utils import generate_unique_slug
from mptt.models import MPTTModel, TreeForeignKey

User = settings.AUTH_USER_MODEL


# from django.contrib.auth import get_user_model
# 分类模型 (使用MPTT优化层级结构)
class Category(MPTTModel):
    id = ShortUUIDField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, verbose_name="文章分类")
    description = models.TextField(
        max_length=200,
        verbose_name="分类描述",
        blank=True,  # 允许空字符串
        null=True,  # 允许 NULL
    )

    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)
    icon = models.CharField(max_length=50, blank=True)  # 分类图标
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ["name"]
        verbose_name_plural = "Categories"

    class Meta:
        verbose_name_plural = "分类"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or not self.slug.strip():
            self.slug = generate_unique_slug(Category, self.name)
        super().save(*args, **kwargs)


# 标签模型
class Tag(models.Model):
    id = ShortUUIDField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, verbose_name="文章标签")
    description = models.TextField(
        max_length=200,
        verbose_name="标签描述",
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    usage_count = models.IntegerField(default=0, verbose_name="使用次数")
    color = models.CharField(
        max_length=7,
        default="#3498db",
        validators=[RegexValidator(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")],
    )

    class Meta:
        ordering = ["-usage_count", "name"]
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or not self.slug.strip():
            self.slug = generate_unique_slug(Tag, self.name)
        super().save(*args, **kwargs)


# 文章模型
class Article(models.Model):
    STATUS_CHOICES = (
        ("draft", "草稿"),
        ("published", "已发布"),
        ("archived", "归档"),
    )

    REVIEW_CHOICES = (
        ("pending", "待审核"),
        ("approved", "已批准"),
        ("rejected", "已拒绝"),
    )

    id = ShortUUIDField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="文章标题")
    content = models.TextField(verbose_name="文章内容")
    html_content = models.TextField(verbose_name="文章渲染内容")
    excerpt = models.CharField(max_length=200, verbose_name="文章摘要")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")

    categories = models.ManyToManyField(
        Category, related_name="articles", verbose_name="文章分类"
    )
    tags = models.ManyToManyField(Tag, related_name="articles", verbose_name="文章标签")

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft", verbose_name="文章状态"
    )

    review_status = models.CharField(
        max_length=10,
        choices=REVIEW_CHOICES,
        default="pending",
        verbose_name="审核状态",
    )

    reviewer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_articles",
    )

    cover_image = models.ImageField(
        upload_to="article_cover/%Y/%m",
        verbose_name="文章封面图",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif", "webp"])],
    )

    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    views_count = models.IntegerField(default=0, verbose_name="阅读次数")

    # 软删除字段
    is_deleted = models.BooleanField(default=False, verbose_name="已删除")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="删除时间")

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["title"]),
            models.Index(fields=["published_at"]),
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["review_status"]),
            models.Index(fields=["is_deleted"]),
        ]
        verbose_name_plural = "文章"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 生成唯一slug
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1

            while Article.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        # 设置发布时间
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()

        # 如果文章被删除且未设置删除时间
        if self.is_deleted and not self.deleted_at:
            self.deleted_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"slug": self.slug})


# 页面模型
class Page(models.Model):
    PAGE_CHOICES = (
        ("about", "关于页面"),
        ("friend", "友链页面"),
        ("custom", "自定义页面"),
    )

    page_type = models.CharField(
        max_length=10, choices=PAGE_CHOICES, unique=True, verbose_name="页面类型"
    )
    title = models.CharField(max_length=100, verbose_name="页面标题")
    content = models.TextField(verbose_name="页面内容")
    html_content = models.TextField(verbose_name="渲染后内容")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name="是否发布")

    class Meta:
        verbose_name_plural = "页面"

    def __str__(self):
        return self.title


# 友情链接模型 (新增)
class FriendLink(models.Model):
    name = models.CharField(max_length=100, verbose_name="网站名称")
    url = models.URLField(verbose_name="网站地址")
    description = models.TextField(max_length=200, blank=True, verbose_name="网站描述")
    logo = models.ImageField(
        upload_to="friend_links/", blank=True, null=True, verbose_name="网站Logo"
    )
    is_approved = models.BooleanField(default=False, verbose_name="已审核")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "友情链接"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
