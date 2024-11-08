from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.name


class WeatherCache(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    pressure = models.IntegerField()
    wind_speed = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)


class RequestHistory(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
    request_type = models.CharField(max_length=10, choices=[('web', 'Web'), ('telegram', 'Telegram')])

    class Meta:
        ordering = ['-request_time']

    def __str__(self):
        return f"{self.city.name} - {self.request_time} ({self.request_type})"