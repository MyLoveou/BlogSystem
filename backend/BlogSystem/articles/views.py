from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import (
   Category, Tag, Article, Page, FriendLink
)
from .serializers import (
   CategorySerializer, TagSerializer,
   ArticleListSerializer, ArticleDetailSerializer,
   PageSerializer, FriendLinkSerializer
)
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

User = get_user_model()

class CategoryViewSet(viewsets.ModelViewSet):
    """
    分类API端点
    
    管理文章分类，支持树形结构
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # 仅管理员可修改
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    
    def get_queryset(self):
        """优化查询：预取父级分类"""
        return Category.objects.select_related('parent').all()
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取分类树形结构"""
        root_categories = Category.objects.filter(parent__isnull=True)
        serializer = self.get_serializer(root_categories, many=True)
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    """
    标签API端点
    
    管理文章标签，支持按使用次数排序
    """
    queryset = Tag.objects.all().order_by('-usage_count')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]  # 仅管理员可修改
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'usage_count']

class ArticleFilter(filters.FilterSet):
    """文章过滤器"""
    status = filters.ChoiceFilter(choices=Article.STATUS_CHOICES)
    review_status = filters.ChoiceFilter(choices=Article.REVIEW_CHOICES)
    category = filters.ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all()
    )
    tag = filters.ModelChoiceFilter(
        field_name='tags',
        queryset=Tag.objects.all()
    )
    author = filters.ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Article
        fields = ['status', 'review_status', 'category', 'tag', 'author'] # 允许的过滤字段

class ArticleViewSet(viewsets.ModelViewSet):
    filterset_class = ArticleFilter
    queryset = Article.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ArticleFilter
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['published_at', 'created_at', 'updated_at', 'views_count']

    def get_serializer_class(self):
        return ArticleListSerializer if self.action == 'list' else ArticleDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('author', 'reviewer')
        queryset = queryset.prefetch_related('categories', 'tags')
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if serializer.validated_data.get('status') == 'published' and not instance.published_at:
            serializer.save(published_at=timezone.now())
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布文章"""
        article = self.get_object()
        if article.status == 'published':
            return Response({'error': '文章已发布'}, status=status.HTTP_400_BAD_REQUEST)
        
        article.status = 'published'
        article.published_at = timezone.now()
        article.save()
        return Response({'status': '文章已发布'})
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """归档文章"""
        article = self.get_object()
        if article.status == 'archived':
            return Response({'error': '文章已归档'}, status=status.HTTP_400_BAD_REQUEST)
        
        article.status = 'archived'
        article.save()
        return Response({'status': '文章已归档'})
    
    @action(detail=True, methods=['post'])
    def delete(self, request, pk=None):
        """软删除文章"""
        article = self.get_object()
        if article.is_deleted:
            return Response({'error': '文章已删除'}, status=status.HTTP_400_BAD_REQUEST)
        
        article.is_deleted = True
        article.deleted_at = timezone.now()
        article.save()
        return Response({'status': '文章已删除'})
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """恢复已删除的文章"""
        article = self.get_object()
        if not article.is_deleted:
            return Response({'error': '文章未删除'}, status=status.HTTP_400_BAD_REQUEST)
        
        article.is_deleted = False
        article.deleted_at = None
        article.save()
        return Response({'status': '文章已恢复'})
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """审核通过文章"""
        article = self.get_object()
        if article.review_status == 'approved':
            return Response({'error': '文章已审核通过'}, status=status.HTTP_400_BAD_REQUEST)
        
        article.review_status = 'approved'
        article.reviewer = request.user
        article.save()
        return Response({'status': '文章审核通过'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """拒绝文章"""
        article = self.get_object()
        if article.review_status == 'rejected':
            return Response({'error': '文章已拒绝'}, status=status.HTTP_400_BAD_REQUEST)
        
        article.review_status = 'rejected'
        article.reviewer = request.user
        article.save()
        return Response({'status': '文章已拒绝'})

class PageViewSet(viewsets.ModelViewSet):
    """
    页面API端点
    
    管理特殊页面（关于、友链等），按页面类型(page_type)唯一索引
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    # permission_classes = [permissions.IsAdminUser]  # 仅管理员可修改
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'page_type'  # 使用page_type作为查找字段
    
    def get_object(self):
        """重写以支持通过page_type获取对象"""
        page_type = self.kwargs['page_type']
        return get_object_or_404(Page, page_type=page_type)
    
    @action(detail=False, methods=['get'])
    def get_by_type(self, request):
        """通过页面类型获取页面"""
        page_type = request.query_params.get('type')
        if not page_type:
            return Response({'error': '缺少type参数'}, status=status.HTTP_400_BAD_REQUEST)
        
        page = Page.objects.filter(page_type=page_type, is_published=True).first()
        if not page:
            return Response({'error': '未找到页面或页面未发布'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(page)
        return Response(serializer.data)

class FriendLinkViewSet(viewsets.ModelViewSet):
    """
    友情链接API端点
    
    管理友情链接，支持审核状态控制
    """
    queryset = FriendLink.objects.filter(is_approved=True)  # 默认只显示已审核的
    serializer_class = FriendLinkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'url']
    ordering_fields = ['created_at', 'name']
    
    def get_queryset(self):
        """管理员可查看所有链接，普通用户只看已审核的"""
        if self.request.user.is_staff:
            return FriendLink.objects.all()
        return super().get_queryset()
    
    def perform_create(self, serializer):
        """创建时自动设置为待审核状态"""
        serializer.save(is_approved=False)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """审核通过友情链接"""
        link = self.get_object()
        if link.is_approved:
            return Response({'error': '链接已审核通过'}, status=status.HTTP_400_BAD_REQUEST)
        
        link.is_approved = True
        link.save()
        return Response({'status': '链接审核通过'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """拒绝友情链接"""
        link = self.get_object()
        if not link.is_approved:
            return Response({'error': '链接未通过审核'}, status=status.HTTP_400_BAD_REQUEST)
        
        link.is_approved = False
        link.save()
        return Response({'status': '链接已拒绝'})