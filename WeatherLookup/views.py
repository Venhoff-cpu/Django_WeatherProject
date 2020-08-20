from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, View
from .forms import CityForm
import requests


api_url = ' https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a39f896edf10d5de6c18cb86f3ab69aa'
api_url_id = ' https://api.openweathermap.org/data/2.5/weather?id={}&units=metric&' \
             'appid=a39f896edf10d5de6c18cb86f3ab69aa'

# oneshot api call takes parameters longtitude(lon) and latitude(lat) - used for detailed view - forcasts
oneshot_api_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric$lang=pl&' \
          'appid=a39f896edf10d5de6c18cb86f3ab69aa'


def api_context_processor(city):
    if type(city) == str:
        response = requests.get(api_url.format(city)).json()
    else:
        response = requests.get(api_url_id.format(city)).json()
    ctx = {}
    ctx['city'] = response['name']
    ctx['city_id'] = response['id']
    ctx['temperature'] = response['main']['temp']
    ctx['temp_max'] = response['main']['temp_max']
    ctx['temp_min'] = response['main']['temp_min']
    ctx['temp_fell'] = response['main']['feels_like']
    ctx['pressure'] = response['main']['pressure']
    ctx['humidity'] = response['main']['humidity'] # presented in %
    ctx['wind_speed'] = response['wind']['speed']
    ctx['wind_deg'] = response['wind']['deg']
    ctx['clouds'] = response['clouds']['all'] # presented in %
    if 'rain' in response:
        ctx['rain_1h'] = response['rain']['1h']
        ctx['rain_3h'] = response['rain']['3h']
    if 'snow' in response:
        ctx['snow_1h'] = response['snow']['1h']
        ctx['snow_3h'] = response['snow']['3h']
    ctx['description'] = response['weather'][0]['description']
    ctx['sunrise'] = response['sys']['sunrise']
    ctx['sunset'] = response['sys']['sunset']
    ctx['icon'] = response['weather'][0]['icon']

    return ctx


class Index(TemplateView):
    template_name = "WeatherLookup/base.html"


class About(TemplateView):
    template_name = "WeatherLookup/about.html"


class WeatherCurrent(FormView):
    template_name = "WeatherLookup/weather_homepage.html"
    form_class = CityForm

    def form_valid(self, form):
        city = form.cleaned_data.get('name')
        ctx = api_context_processor(city)
        ctx['form'] = form
        return render(self.request, "WeatherLookup/weather_homepage.html", ctx)


class WeatherDetail(TemplateView):
    template_name = 'WeatherLookup/weather_detail.html'

    def get_context_data(self, **kwargs):
        city_id = kwargs['city_id']
        ctx = api_context_processor(city_id)
        return ctx
