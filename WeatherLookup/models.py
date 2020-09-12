from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64, null=False)
    city_id = models.IntegerField()
    lon = models.IntegerField()
    lat = models.IntegerField()
    fav = models.ManyToManyField(User, through='Favorite')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "cities"


class Favorite(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("city", "user")


class Stations(models.Model):
    station_id = models.IntegerField(null=False, primary_key=True)
    address_street = models.TextField(blank=True, null=True)
    city_commune_communeName = models.TextField()
    city_commune_districtName = models.TextField()
    city_commune_provinceName = models.TextField()
    station_city_id = models.IntegerField()
    city_name = models.CharField(max_length=128)
    gegrLat = models.FloatField()
    gegrLon = models.FloatField()
    station_name = models.CharField(max_length=128)


class Sensors(models.Model):
    sensor_id = models.IntegerField(null=False, primary_key=True)
    param_id = models.IntegerField()
    param_code = models.CharField(max_length=8)
    param_formula = models.CharField(max_length=256)
    param_name = models.CharField(max_length=256)
    station = models.ForeignKey(Stations, on_delete=models.CASCADE)


class Readings(models.Model):
    sensor = models.ForeignKey(Sensors, on_delete=models.CASCADE)
    datetime = models.DateTimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = (('sensor_id', 'datetime'),)


class AirIndex(models.Model):
    station = models.ForeignKey(Stations, on_delete=models.CASCADE)
    index_date = models.DateTimeField()
    index_levelID = models.IntegerField()
    index_levelName = models.CharField(max_length=32)

    class Meta:
        unique_together = (('station_id', 'index_date'),)
