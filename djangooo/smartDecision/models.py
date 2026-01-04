from django.db import models

class Sensor(models.Model):
    # 传感器类型定义
    SENSOR_TYPES = [
        ('TEMP', '温度传感器'),
        ('HUMI', '湿度传感器'),
        ('CO2', '二氧化碳传感器'),
        ('NH3', '氨气传感器'),
        ('WATT', '能耗传感器'),
    ]

    name = models.CharField(max_length=100, verbose_name='传感器名称')
    sensor_type = models.CharField(max_length=10, choices=SENSOR_TYPES, default='TEMP', verbose_name='传感器类型')
    location = models.CharField(max_length=100, verbose_name='安装区域(如: 1号猪舍/A区)')
    unit = models.CharField(max_length=20, verbose_name='计量单位(如: ℃, %, ppm)')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.location})"

class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    # 冗余存储传感器名称或位置，方便快照查看，类似于你之前的 appliance_name
    sensor_name_snapshot = models.CharField(max_length=100, verbose_name='传感器名称快照')
    
    # 将原本的 usage (用电量) 改为 value (监测数值)
    value = models.FloatField(verbose_name='监测数值')
    
    # 养殖场通常需要更精细的时间维度（不仅是日期，还有具体时间点）
    timestamp = models.DateTimeField(verbose_name='监测时间')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # 如果是记录历史轨迹，通常不设置 unique_together。
        # 但如果是记录“日平均值”，则保留 unique_together = ['sensor', 'date']
        verbose_name = '传感器读数'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.sensor.name} - {self.timestamp}: {self.value}{self.sensor.unit}"