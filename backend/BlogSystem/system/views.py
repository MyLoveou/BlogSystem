from .serializers import SiteConfigSerializer, NavMenuSerializer, LoginSerializer
from .models import SiteConfig, NavMenu
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from django.db import models
# from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
# from rest_framework.views import APIView
# from rest_framework.response import Response
# Create your views here.
class SiteConfigViewSet(viewsets.ModelViewSet):
    """
    站点配置API端点
    
    提供对站点配置的CRUD操作
    配置键(key)是唯一的，用于存储如网站标题、标语等全局设置
    """
    queryset = SiteConfig.objects.all()
    serializer_class = SiteConfigSerializer
    permission_classes = [permissions.IsAdminUser]  # 仅管理员可配置
    lookup_field = 'key'  # 使用key作为查找字段
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  # 禁用HEAD等
    
    def get_object(self):
        """重写以支持通过key获取对象"""
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        key = self.kwargs[lookup_url_kwarg]
        return get_object_or_404(SiteConfig, key=key)
    
    @action(detail=False, methods=['get'])
    def get_by_key(self, request):
        """通过键名获取配置值"""
        key = request.query_params.get('key')
        if not key:
            return Response({'error': '缺少key参数'}, status=status.HTTP_400_BAD_REQUEST)
        
        config = SiteConfig.objects.filter(key=key).first()
        if not config:
            return Response({'error': '未找到配置'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(config)
        return Response(serializer.data)

class NavMenuViewSet(viewsets.ModelViewSet):
    """
    导航菜单API端点
    
    管理网站导航菜单项，支持排序和激活状态控制
    """
    queryset = NavMenu.objects.all().order_by('order')
    serializer_class = NavMenuSerializer
    permission_classes = [permissions.IsAdminUser]  # 仅管理员可修改
    
    def perform_create(self, serializer):
        """创建时自动设置排序值为当前最大值+1"""
        max_order = NavMenu.objects.aggregate(models.Max('order'))['order__max'] or 0
        serializer.save(order=max_order + 1)

class LoginView(APIView):
    """
    登录接口：POST username & password -> access + refresh
    """
    permission_classes = []          # 允许匿名访问
    authentication_classes = []      # 禁用任何认证
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # 生成 JWT 令牌
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response({
                    'detail': '登录成功',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             login(request, user)  # 登录用户并更新 last_login
#             return Response({'detail': '登录成功'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)