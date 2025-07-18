# Generated by Django 5.2.4 on 2025-07-18 06:28

import django.core.validators
import django.db.models.deletion
import mptt.fields
import shortuuidfield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FriendLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="网站名称")),
                ("url", models.URLField(verbose_name="网站地址")),
                (
                    "description",
                    models.TextField(
                        blank=True, max_length=200, verbose_name="网站描述"
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="friend_links/",
                        verbose_name="网站Logo",
                    ),
                ),
                (
                    "is_approved",
                    models.BooleanField(default=False, verbose_name="已审核"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "友情链接",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "page_type",
                    models.CharField(
                        choices=[
                            ("about", "关于页面"),
                            ("friend", "友链页面"),
                            ("custom", "自定义页面"),
                        ],
                        max_length=10,
                        unique=True,
                        verbose_name="页面类型",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="页面标题")),
                ("content", models.TextField(verbose_name="页面内容")),
                ("html_content", models.TextField(verbose_name="渲染后内容")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="是否发布"),
                ),
            ],
            options={
                "verbose_name_plural": "页面",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    shortuuidfield.fields.ShortUUIDField(
                        blank=True,
                        editable=False,
                        max_length=22,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="文章标签"
                    ),
                ),
                (
                    "description",
                    models.TextField(max_length=200, verbose_name="标签描述"),
                ),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "usage_count",
                    models.IntegerField(default=0, verbose_name="使用次数"),
                ),
                (
                    "color",
                    models.CharField(
                        default="#3498db",
                        max_length=7,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
                            )
                        ],
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "标签",
                "ordering": ["-usage_count", "name"],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    shortuuidfield.fields.ShortUUIDField(
                        blank=True,
                        editable=False,
                        max_length=22,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="文章分类"
                    ),
                ),
                (
                    "description",
                    models.TextField(max_length=200, verbose_name="分类描述"),
                ),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("icon", models.CharField(blank=True, max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="articles.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "分类",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    shortuuidfield.fields.ShortUUIDField(
                        blank=True,
                        editable=False,
                        max_length=22,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="文章标题")),
                ("content", models.TextField(verbose_name="文章内容")),
                ("html_content", models.TextField(verbose_name="文章渲染内容")),
                ("excerpt", models.CharField(max_length=200, verbose_name="文章摘要")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "草稿"),
                            ("published", "已发布"),
                            ("archived", "归档"),
                        ],
                        default="draft",
                        max_length=10,
                        verbose_name="文章状态",
                    ),
                ),
                (
                    "review_status",
                    models.CharField(
                        choices=[
                            ("pending", "待审核"),
                            ("approved", "已批准"),
                            ("rejected", "已拒绝"),
                        ],
                        default="pending",
                        max_length=10,
                        verbose_name="审核状态",
                    ),
                ),
                (
                    "cover_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="article_cover/%Y/%m",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["jpg", "jpeg", "png", "gif", "webp"]
                            )
                        ],
                        verbose_name="文章封面图",
                    ),
                ),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                (
                    "views_count",
                    models.IntegerField(default=0, verbose_name="阅读次数"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="已删除"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="删除时间"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "reviewer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviewed_articles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="articles",
                        to="articles.category",
                        verbose_name="文章分类",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        related_name="articles",
                        to="articles.tag",
                        verbose_name="文章标签",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "文章",
                "ordering": ("-created_at",),
                "indexes": [
                    models.Index(fields=["slug"], name="articles_ar_slug_452037_idx"),
                    models.Index(
                        fields=["created_at"], name="articles_ar_created_b5cc75_idx"
                    ),
                    models.Index(fields=["title"], name="articles_ar_title_ee81af_idx"),
                    models.Index(
                        fields=["published_at"], name="articles_ar_publish_a51805_idx"
                    ),
                    models.Index(
                        fields=["status", "published_at"],
                        name="articles_ar_status_7759bd_idx",
                    ),
                    models.Index(
                        fields=["review_status"], name="articles_ar_review__42c5cc_idx"
                    ),
                    models.Index(
                        fields=["is_deleted"], name="articles_ar_is_dele_b8b6ef_idx"
                    ),
                ],
            },
        ),
    ]
