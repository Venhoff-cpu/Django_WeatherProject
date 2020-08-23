from django.contrib import admin
from django.urls import path
from .views import About, Index, WeatherCurrent, WeatherDetail, WeatherForcast, RegisterView, LoginView, LogoutView


urlpatterns = [
    path('weather/', WeatherCurrent.as_view(), name="index"),
    path('weather/register/', RegisterView.as_view(), name='register'),
    path('weather/login/', LoginView.as_view(), name='login'),
    path('wether/logout/', LogoutView.as_view(), name='logout'),
    path('weather/about/', About.as_view(), name="about"),
    path('weather/detail/<int:city_id>', WeatherDetail.as_view(), name="weather_detail"),
    path('weather/forecast/<int:city_id>', WeatherForcast.as_view(), name='weather_forecast'),
]
