# Django_WeatherProject
Django Training project showing:
* current and forecasted whether using OpenWeatherMap(OWM) API,
* air quality in Poland using data from [GIOŚ (Główny Inspektorat Ochrony Środowiska)](http://www.gios.gov.pl/pl/stan-srodowiska/monitoring-jakosci-powietrza)

## Requirements

Essential:
* Python 3.6
* Django 3.1
* pip
* PostgreSQL9.5+
* MatPlotLib 3.3.1
* NumPy 1.19.1
* Pandas 1.1.1

## Configuration 
Look at **settings.py** file, you will find the following section in it:

```python
try:
    from your.local_settings import DATABASES
except ModuleNotFoundError:
    print("Brak konfiguracji bazy danych w pliku local_settings.py!")
    print("Uzupełnij dane i spróbuj ponownie!")
    exit(0)
```

This means that Django will try to import
The constant `DATABASES` from the file **local_settings.py**. Keep the data for connection there.
Do not put this file under Git's control.

In **local_settings.py** you should also include:
```python
# Secret key
sk = 'yours_secret_key'

# OWM API key
api_key = "yours_OWM_api_key"
```
You can get OWM Api key from here: [OpenWeatherMap](https://openweathermap.org/api).
You need to sign up to get the key.

## Status

Currently working on Air quality part. TODO:
- Prepare a periodic task for updating tables regarding Air quality (Stations, Sensors, Readings, AirIndex)
- Views and templates update.


