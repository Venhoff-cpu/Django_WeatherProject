from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64, null=False)
    city_id = models.IntegerField()
    lon = models.IntegerField()
    lat = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "cities"
        unique_together = ("city_id", "user")
