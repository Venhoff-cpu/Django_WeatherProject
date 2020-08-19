from django.contrib import admin
from django.urls import path
from .views import About, Index


urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('about/', About.as_view(), name="about"),
]
