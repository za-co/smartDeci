from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import SensorData

def latest_status(request):
    data = SensorData.objects.last()

    # 评估规则
    status = "正常"
    if data.temperature > 30 or data.ammonia > 2:
        status = "异常"

    return JsonResponse({
        "temperature": data.temperature,
        "humidity": data.humidity,
        "ammonia": data.ammonia,
        "status": status,
        "time": data.create_time
    })