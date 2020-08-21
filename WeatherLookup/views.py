from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, View
from .forms import CityForm
from .api_processor import api_current_ctx_processor, api_forecast_processor, fetch_current_data, fetch_forecast_data, \
    get_city_name


class Index(TemplateView):
    template_name = "WeatherLookup/base.html"


class About(TemplateView):
    template_name = "WeatherLookup/about.html"


class WeatherCurrent(FormView):
    template_name = "WeatherLookup/weather_homepage.html"
    form_class = CityForm

    def form_valid(self, form):
        city = form.cleaned_data.get('name')
        data = fetch_current_data(city)
        if data:
            ctx = api_current_ctx_processor(data)
        ctx['form'] = form
        return render(self.request, "WeatherLookup/weather_homepage.html", ctx)


class WeatherDetail(TemplateView):
    template_name = 'WeatherLookup/weather_detail.html'

    def get_context_data(self, **kwargs):
        city_id = kwargs['city_id']
        data = fetch_current_data(city_id)
        if data:
            ctx = api_current_ctx_processor(data)
        return ctx


class WeatherForcast(TemplateView):
    template_name = 'WeatherLookup/weather_forecast.html'

    def get_context_data(self, **kwargs):
        ctx = {}
        city_id = kwargs['city_id']
        temp_data = fetch_current_data(city_id)
        lon = temp_data['coord']['lon']
        lat = temp_data['coord']['lat']
        data = fetch_forecast_data(lat, lon)
        if data:
            city_name = get_city_name(temp_data)
            ctx['city'] = city_name
            ctx['table'] = api_forecast_processor(data).to_html(index=False, classes='table')
        return ctx
