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
