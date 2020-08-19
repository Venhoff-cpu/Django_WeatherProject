from django.contrib import admin
from django.urls import path
from .views import About, Index, WeatherCity


urlpatterns = [
    path('weather/', WeatherCity.as_view(), name="index"),
    path('weather/about/', About.as_view(), name="about"),
]
