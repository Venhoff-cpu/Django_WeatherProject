from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import CityForm
import requests


api_url = ' https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a39f896edf10d5de6c18cb86f3ab69aa'
oneshot_api_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric$lang=pl&' \
          'appid=a39f896edf10d5de6c18cb86f3ab69aa'


class Index(TemplateView):
    template_name = "WeatherLookup/base.html"


class About(TemplateView):
    template_name = "WeatherLookup/about.html"


class WeatherCity(FormView):
    template_name = "WeatherLookup/weather_city.html"
    form_class = CityForm

    def form_valid(self, form):
        city = form.cleaned_data.get('name')
        response = requests.get(api_url.format(city)).json()
        ctx = {}
        ctx['form'] = form
        ctx['city'] = city
        ctx['temperature'] = response['main']['temp']
        ctx['description'] = response['weather'][0]['description']
        ctx['icon'] = response['weather'][0]['icon']
        return render(self.request, "WeatherLookup/weather_city.html", ctx)


