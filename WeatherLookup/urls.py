from django.contrib import admin
from django.urls import path
from .views import About, Index, WeatherCurrent, WeatherDetail


urlpatterns = [
    path('weather/', WeatherCurrent.as_view(), name="index"),
    path('weather/about/', About.as_view(), name="about"),
    path('weather/detail/<int:city_id>', WeatherDetail.as_view(), name="weather_detail")
]
