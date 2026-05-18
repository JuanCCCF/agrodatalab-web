from django.db import models

# Create your models here.
class EnviroProRecord(models.Model):
    fecha = models.DateTimeField()
    humedad_media = models.FloatField()
    temp_suelo = models.FloatField()
    temp_max = models.FloatField()
    temp_min = models.FloatField()
    bateria = models.FloatField()
    panel_solar = models.FloatField()
    observaciones = models.TextField(blank=True)
