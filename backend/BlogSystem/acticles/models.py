from django.db import models
from shortuuidfield import ShortUUIDField
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
# from BlogSystem import settings
from django.conf import settings  # 导入 settings


# 分类模型
class Category(models.Model):
    # id = model.
    id = ShortUUIDField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, verbose_name="文章分类")
    description = models.TextField(max_length=200, unique=True, verbose_name="分类描述")
    slug = models.SlugField(max_length=100, unique=True)  # url友好标识符
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )  # 父级分类
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# 标签模型
class Tag(models.Model):
    id = ShortUUIDField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, verbose_name="文章标签")
    description = models.TextField(max_length=200, unique=True, verbose_name="标签描述")
    slug = models.SlugField(max_length=100, unique=True)  # url友好标识符
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    usege_count = models.IntegerField(default=0, verbose_name="使用次数")
    color = models.CharField(max_length=7, default='#3498db')  # 标签颜色

    class Meta:
        ordering = ["-usage_count", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# 文章模型
class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '归档'),
    )

    id = ShortUUIDField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="文章标题")

    content = models.TextField(verbose_name="文章内容")
    html_content = models.TextField(verbose_name="文章渲染内容")

    excerpt = models.CharField(max_length=200, verbose_name="文章摘要")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1,  # 假设超级用户ID是1
    )
    category = models.ManyToManyField(Category, related_name='articles', verbose_name="文章分类")
    tags = models.ManyToManyField(Tag, related_name='tags', verbose_name="文章标签")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="文章状态")

    cover_image = models.ImageField(
        upload_to="article_cover/", verbose_name="文章封面图", blank=True, null=True
    )
    slug = models.SlugField(max_length=100, unique=True)  # url友好标识符

    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间

    views_count = models.IntegerField(default=0, verbose_name="阅读次数")

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"slug": self.slug})
