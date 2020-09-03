import requests
import collections
from .utils import unix_to_datetime, unix_to_datetime_hour
from Django_WeatherProject.local_settings import api_key
import pandas as pd


api_current_url = (
    "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
)
api_current_url_id = (
    " https://api.openweathermap.org/data/2.5/weather?id={}&units=metric&appid={}"
)
api_forecast_url_id = (
    "api.openweathermap.org/data/2.5/forecast?id={}$units=metric&appid={}"
)


# oneshot api call takes parameters longtitude(lon) and latitude(lat) - used for 5 day forecast and hourly forcast
forecast_api_url = (
    "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=current,minutely&appid={}"
)


def get_wind_direction(degree):
    """
    Convert wind degree to direction.
    :param degree: degree of the wind (float).
    :return direction of the wind (N, NNE, NE, etc) in str.
    """
    DEGREES = [-11.25, 11.25, 33.75, 56.25,
               78.75, 101.25, 123.75, 146.25,
               168.75, 191.25, 213.75, 236.25,
               258.75, 281.25, 303.75, 326.25, 348.75]

    DIRECTIONS = ['N', 'NNE', 'NE', 'ENE',
                  'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW',
                  'W', 'WNW', 'NW', 'NNW']

    # Correction for North wind.
    if degree > 348.75:
        degree -= 360

    for i in range(len(DIRECTIONS)):
        left_border = DEGREES[i]
        right_border = DEGREES[i + 1]

        if left_border < degree <= right_border:
            return DIRECTIONS[i]


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
    """
    Extraction of json data - current weather
    :param data: API response from OpeanWeathermap.org in json format
    :return Dictionary of lists
    """
    ctx = {}
    ctx["city_name"] = data["name"]
    ctx["city_id"] = data["id"]
    ctx["temperature"] = data["main"]["temp"]
    ctx["temp_max"] = data["main"]["temp_max"]
    ctx["temp_min"] = data["main"]["temp_min"]
    ctx["temp_fell"] = data["main"]["feels_like"]
    ctx["pressure"] = data["main"]["pressure"]
    ctx["humidity"] = data["main"]["humidity"]  # presented in %
    ctx["wind_speed"] = data["wind"]["speed"]
    ctx["wind_deg"] = get_wind_direction(data["wind"]["deg"])
    ctx["clouds"] = data["clouds"]["all"]  # presented in %
    if "rain" in data:
        ctx["rain_1h"] = data["rain"]["1h"]
        if "3h" in data["rain"]:
            ctx["rain_3h"] = data["rain"]["3h"]
    if "snow" in data:
        ctx["snow_1h"] = data["snow"]["1h"]
        if "3h" in data["snow"]:
            ctx["snow_3h"] = data["snow"]["3h"]
    ctx["description"] = data["weather"][0]["description"]
    ctx["sunrise"] = data["sys"]["sunrise"]
    ctx["sunset"] = data["sys"]["sunset"]
    ctx["icon"] = data["weather"][0]["icon"]

    return ctx


def api_forecast_processor(data):
    """
    Extraction of json data - 5 day forecast
    :param data: API response from OpeanWeathermap.org in json format
    :return: Dictionary of lists
    """
    ctx = collections.defaultdict(list)
    for forecast in data["daily"]:
        date = unix_to_datetime(forecast["dt"])
        ctx["date"].append(date)
        ctx["temp_day"].append(forecast["temp"]["day"])
        ctx["temp_night"].append(forecast["temp"]["night"])
        ctx["pressure"].append(forecast["pressure"])
        ctx["humidity"].append(forecast["humidity"])
        ctx["weather_description"].append(forecast["weather"][0]["description"])
        ctx["clouds"].append(forecast["clouds"])
        ctx["wind_speed_prediction"].append(forecast["wind_speed"])
        ctx["wind_degree_prediction"].append(get_wind_direction(forecast["wind_deg"]))
        ctx["pop_chance"].append(forecast["pop"])
        if "rain" in forecast:
            ctx["rainfall"].append(forecast["rain"])
        else:
            ctx["rainfall"].append(0)
        if "snow" in forecast:
            ctx["snowfall"].append(forecast["snow"])
        else:
            ctx["snowfall"].append(0)

    return ctx


def get_df_forecast(ctx):
    """
    Creating dataframe of forecast
    :param ctx: context - dictionary of lists
    :return: Pandas dataframe
    """
    df_ctx = pd.DataFrame()
    df_ctx["date"] = ctx["date"]
    df_ctx["temp_day"] = ctx["temp_day"]
    df_ctx["temp_night"] = ctx["temp_night"]
    df_ctx["Pressure"] = ctx["pressure"]
    df_ctx["Humidity"] = ctx["humidity"]
    df_ctx["Description"] = ctx["weather_description"]
    df_ctx["Cloudiness"] = ctx["clouds"]
    df_ctx["Wind speed"] = ctx["wind_speed_prediction"]
    df_ctx["Wind direction"] = ctx["wind_degree_prediction"]
    df_ctx["Chance of precipitation"] = ctx["pop_chance"]
    df_ctx["Rainfall"] = ctx["rainfall"]
    df_ctx["Snowfall"] = ctx["snowfall"]

    return df_ctx


def get_hourly_temperature(data):
    """
    Extraction of json data - Only hourly temperature 48h
    :param data: API response from OpeanWeathermap.org in json format
    :return: dict of lists
    """
    ctx = collections.defaultdict(list)
    for forecast in data["hourly"]:
        date = unix_to_datetime_hour(forecast["dt"])
        ctx["date"].append(date)
        ctx["temp"].append(forecast["temp"])

    return ctx


def get_city_name(data):
    """
    Function to extract only the name of the city.
    :param data: API response from fetch_current_data
    :return: City name
    """
    return data["name"]
