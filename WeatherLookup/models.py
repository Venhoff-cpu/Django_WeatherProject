from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
