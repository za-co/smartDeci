from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Sensor, SensorReading
from .serializers import SensorSerializer, SensorReadingSerializer

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    @action(detail=False, methods=['post'])
    def upload_batch_data(self, request):
        """
        接收物联网网关批量上传的数据
        """
        data = request.data
        sensor_id = data.get('sensor_id')
        readings = data.get('readings', [])

        try:
            with transaction.atomic():
                sensor = Sensor.objects.get(pk=sensor_id)
                # 批量构造对象
                reading_objects = [
                    SensorReading(
                        sensor=sensor,
                        sensor_name_snapshot=sensor.name,
                        value=item.get('value'),
                        timestamp=item.get('timestamp')
                    ) for item in readings
                ]
                SensorReading.objects.bulk_create(reading_objects)
                return Response({"msg": f"成功记录{len(reading_objects)}条数据"}, status=status.HTTP_201_CREATED)
        except Sensor.DoesNotExist:
            return Response({"error": "传感器未注册"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def smart_farm_report(self, request):
        """
        【决策支持中心】
        直接利用 SensorSerializer 的 current_status 字段
        返回全场传感器的智能评估报告
        """
        # 获取所有启用的传感器，并预加载最新的读数以提高查询效率
        sensors = Sensor.objects.filter(is_active=True).prefetch_related('readings')
        
        # 序列化器会自动运行 get_current_status 中的 if/else 逻辑
        serializer = self.get_serializer(sensors, many=True)
        
        # 统计全场预警概览
        report_data = serializer.data
        alert_count = sum(1 for item in report_data if item['current_status']['level'] in ['red', 'orange'])
        
        return Response({
            "timestamp": timezone.now(),
            "summary": {
                "total_sensors": len(report_data),
                "alert_sensors": alert_count,
                "health_score": max(0, 100 - alert_count * 20) # 简单的健康评分算法
            },
            "detail": report_data
        })

    @action(detail=True, methods=['get'])
    def high_frequency_analysis(self, request, pk=None):
        """
        特定传感器的精细化决策分析
        """
        sensor = self.get_object()
        # 调用序列化器获取过去24小时的所有高频数据
        serializer = self.get_serializer(sensor)
        
        # 提取数据供前端直接绘图
        readings = serializer.data['recent_readings']
        values = [r['value'] for r in readings]
        
        return Response({
            "info": serializer.data,
            "analytics": {
                "trend": "上升" if len(values) > 2 and values[-1] > values[0] else "下降/平稳",
                "volatility": round(max(values) - min(values), 2) if values else 0 # 计算波动率
            }
        })
    @action(detail=False, methods=['get'])
    def smart_farm_report(self, request):
        """
        优化后的决策报告：采用加权扣分制
        """
        sensors = Sensor.objects.filter(is_active=True)
        serializer = self.get_serializer(sensors, many=True)
        report_data = serializer.data
        
        total_deduction = 0
        alert_sensors_count = 0
        
        for sensor_data in report_data:
            impact = sensor_data['current_status'].get('score_impact', 0)
            if impact > 0:
                total_deduction += impact
                alert_sensors_count += 1
        
        # 基础分100，扣完为止
        health_score = max(0, 100 - total_deduction)
        
        return Response({
            "timestamp": timezone.now(),
            "summary": {
                "total_sensors": len(report_data),
                "alert_sensors": alert_sensors_count,
                "health_score": health_score,
                "status_label": "优" if health_score >= 90 else "良" if health_score >= 70 else "差"
            },
            "detail": report_data
        })
    
# 2. 注册视图
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({"error": "用户名和密码不能为空"}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "该用户名已存在"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 创建用户
    user = User.objects.create_user(username=username, password=password)
    return Response({"msg": "注册成功", "user_id": user.id}, status=status.HTTP_201_CREATED)

# 3. 登录视图
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({"msg": "登录成功", "username": user.username}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "用户名或密码错误"}, status=status.HTTP_401_UNAUTHORIZED)