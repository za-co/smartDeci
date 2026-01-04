from rest_framework import serializers
from .models import Sensor, SensorReading
from datetime import timedelta
from django.utils import timezone

# 1. 传感器读数的序列化器
class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        # 养殖场数据需要精确到时间点，所以返回 timestamp
        fields = ['timestamp', 'value'] 

# 2. 传感器及其运行状态的序列化器
class SensorSerializer(serializers.ModelSerializer):
    # 获取最近 24 小时的高频监测数据
    recent_readings = serializers.SerializerMethodField()
    # 获取当前最新的状态（智能评估结果）
    current_status = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'sensor_type', 'location', 'unit', 'recent_readings', 'current_status']

    def get_recent_readings(self, obj):
        """获取传感器最近 24 小时的原始读数数据"""
        day_ago = timezone.now() - timedelta(hours=24)
        readings = obj.readings.filter(timestamp__gte=day_ago).order_by('timestamp')
        return SensorReadingSerializer(readings, many=True).data

    def get_current_status(self, obj):
        """
        核心决策逻辑：
        根据最后一条读数，给前端返回评估结论和颜色标识（用于前端 UI 告警）
        """
        last_reading = obj.readings.order_by('-timestamp').first()
        if not last_reading:
            return {"assessment": "无数据", "level": "gray"}

        val = last_reading.value
        # 智能评估逻辑（示例：温度）
        if obj.sensor_type == 'TEMP':
            if val > 30:
                return {"assessment": "温度过高", "level": "red", "suggestion": "开启湿帘降温"}
            if val < 15:
                return {"assessment": "温度过低", "level": "blue", "suggestion": "开启暖风机"}
            return {"assessment": "舒适", "level": "green", "suggestion": "环境良好"}
        
        # 示例：氨气浓度 (NH3)
        elif obj.sensor_type == 'NH3':
            if val > 20:
                return {"assessment": "氨气超标", "level": "orange", "suggestion": "加强强制通风"}
            return {"assessment": "清新", "level": "green", "suggestion": "空气质量优良"}

        return {"assessment": "正常监测中", "level": "green"}