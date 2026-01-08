from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet, login_view, register_view,user_info_view

# 1. 创建路由器并注册 ViewSet
router = DefaultRouter()
# 此时生成的路径前缀是 sensors/
router.register(r'sensors', SensorViewSet, basename='sensor')

# 统一大路由api/
urlpatterns = [
    # A. 路由器生成的 URL (涵盖了传感器增删改查及智能报告)
    path('', include(router.urls)),

    # B. 手动定义的视图（登录、注册等基础功能）
    path('login/', login_view),
    path('register/', register_view),
    path('user/info/', user_info_view), # 新增
]