from django.contrib import admin
from django.urls import path
from .views import Index, About

urlpatterns = [
    path('air/', Index.as_view(), name="index"),
    path('air/about/', About.as_view(), name="about"),
]
