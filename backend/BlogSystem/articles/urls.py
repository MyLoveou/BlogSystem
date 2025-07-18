from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ArticleViewSet, TagViewSet, PageViewSet, FriendLinkViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'tags', TagViewSet)
router.register(r'pages', PageViewSet)
router.register(r'friendlinks', FriendLinkViewSet)


urlpatterns = [
    path('', include(router.urls)),
]