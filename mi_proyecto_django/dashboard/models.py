from django.db import models

# Create your models here.
class RegistroHumedad(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    humedad   = models.IntegerField()

    def __str__(self):
        return f"{self.timestamp} - {self.humedad}%"