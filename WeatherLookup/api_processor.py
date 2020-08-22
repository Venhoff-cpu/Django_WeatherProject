import requests
import collections
from .utils import unix_to_datetime
import pandas as pd

api_key = 'a39f896edf10d5de6c18cb86f3ab69aa'
api_current_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
api_current_url_id = ' https://api.openweathermap.org/data/2.5/weather?id={}&units=metric&' \
             'appid={}'
api_forecast_url_id = 'api.openweathermap.org/data/2.5/forecast?id={}$units=metric&appid={} '


# oneshot api call takes parameters longtitude(lon) and latitude(lat) - used for 5 day forecast
forecast_api_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric$lang=pl&' \
                   'exclude=current,minutely,hourly&appid={}'


def fetch_current_data(city):
    if isinstance(city, str):
        response = requests.get(api_current_url.format(city, api_key)).json()
    else:
        response = requests.get(api_current_url_id.format(city, api_key)).json()

    return response


def fetch_forecast_data(lat, lon):
    response = requests.get(forecast_api_url.format(lat, lon, api_key)).json()
    return response


def api_current_ctx_processor(data):
    ctx = {}
    ctx['city'] = data['name']
    ctx['city_id'] = data['id']
    ctx['temperature'] = data['main']['temp']
    ctx['temp_max'] = data['main']['temp_max']
    ctx['temp_min'] = data['main']['temp_min']
    ctx['temp_fell'] = data['main']['feels_like']
    ctx['pressure'] = data['main']['pressure']
    ctx['humidity'] = data['main']['humidity'] # presented in %
    ctx['wind_speed'] = data['wind']['speed']
    ctx['wind_deg'] = data['wind']['deg']
    ctx['clouds'] = data['clouds']['all'] # presented in %
    if 'rain' in data:
        ctx['rain_1h'] = data['rain']['1h']
        ctx['rain_3h'] = data['rain']['3h']
    if 'snow' in data:
        ctx['snow_1h'] = data['snow']['1h']
        ctx['snow_3h'] = data['snow']['3h']
    ctx['description'] = data['weather'][0]['description']
    ctx['sunrise'] = data['sys']['sunrise']
    ctx['sunset'] = data['sys']['sunset']
    ctx['icon'] = data['weather'][0]['icon']

    return ctx


def api_forecast_processor(data):
    """
    Extraction of json data
    :param data: API response from OpeanWeathermap.org in json fomat
    :return: Dictionary of lists
    """
    ctx = collections.defaultdict(list)
    for forecast in data['daily']:
        date = unix_to_datetime(forecast['dt'])
        ctx['date'].append(date)
        ctx['temp_day'].append(forecast['temp']['day'])
        ctx['temp_night'].append(forecast['temp']['night'])
        ctx['pressure'].append(forecast['pressure'])
        ctx['humidity'].append(forecast['humidity'])
        ctx['weather_description'].append(forecast['weather'][0]['description'])
        ctx['clouds'].append(forecast['clouds'])
        ctx['wind_speed_prediction'].append(forecast['wind_speed'])
        ctx['wind_degree_prediction'].append(forecast['wind_deg'])
        ctx['pop_chance'].append(forecast['pop'])
        if 'rain' in forecast:
            ctx['rainfall'].append(forecast['rain'])
        else:
            ctx['rainfall'].append(0)
        if 'snow' in forecast:
            ctx['snowfall'].append(forecast['snow'])
        else:
            ctx['snowfall'].append(0)

    df_ctx = pd.DataFrame()
    df_ctx['date'] = ctx['date']
    df_ctx['temp_day'] = ctx['temp_day']
    df_ctx['temp_night'] = ctx['temp_night']
    df_ctx['pressure'] = ctx['pressure']
    df_ctx['humidity'] = ctx['humidity']
    df_ctx['weather_description'] = ctx['weather_description']
    df_ctx['clouds'] = ctx['clouds']
    df_ctx['wind_speed_prediction'] = ctx['wind_speed_prediction']
    df_ctx['wind_degree_prediction'] = ctx['wind_degree_prediction']
    df_ctx['pop_chance'] = ctx['pop_chance']
    df_ctx['rainfall'] = ctx['rainfall']
    df_ctx['snowfall'] = ctx['snowfall']

    return df_ctx




def get_city_name(data):
    """
    Function to extract only the name of the city.
    :param data: API response from fecth_current_data
    :return: City name
    """
    return data['name']