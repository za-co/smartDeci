from django.db import models

# Create your models here.

class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    ammonia = models.FloatField()
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'sensor_data'