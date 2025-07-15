from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WeatherCacheViewSet,
    ImageUploadViewSet,
)

router = DefaultRouter()
router.register('weathercache', WeatherCacheViewSet, basename='weathercache')
router.register('imageupload', ImageUploadViewSet, basename='imageupload')


urlpatterns = [
    path('', include(router.urls)),
]