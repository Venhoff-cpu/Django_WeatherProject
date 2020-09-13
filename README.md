# Django_WeatherProject
Django Training project showing:
* current and forecasted whether using OpenWeatherMap(OWM) API,
* air quality in Poland using data from [GIOŚ (Główny Inspektorat Ochrony Środowiska)](http://www.gios.gov.pl/pl/stan-srodowiska/monitoring-jakosci-powietrza)

## Requirements

To install all nesccesery iteams use following command line in terminal
while your virtual enviroment for this project is active:
```python
$ pip install -r requirements.txt
```

## Configuration 
### Database and OWM api
Look at **settings.py** file, you will find the following section in it:

```python
try:
    from your.local_settings import DATABASES
except ModuleNotFoundError:
    print("No database configuration in local_settings.py!")
    print("Fill in the data and try again!")
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

### GIOŚ API

The GIOŚ API along with all current readings is available for public viewing according to the principle of access to 
environmental information for the public.

More information about API: [https://powietrze.gios.gov.pl/pjp/content/api](https://powietrze.gios.gov.pl/pjp/content/api)

### Celery - asynchronous task queue

In the project Celery was used to update air quality data. 
Redis was used as a broker.

By default, the update is to take place every hour, 10 minutes after a full hour 
i.e. 15:10, 16:10, 17:10 etc. You can change the frequency of the task by changing the 
**'schedule'** key in **settings.py** into **CELERY_BEAT_SCHEDULE**.
```python
CELERY_BEAT_SCHEDULE = {
    'update_db': {
        'task': 'WeatherLookup.tasks.update_air_quality_db',
        'schedule': crontab(minute='10', hour='*/1'),
    },
}
```

It is not recommended to run a task every full hour - every full hour there is an update of the readings on the side 
of the Chief Inspectorate, so the obtained data may be incomplete (some sensors have n readings and some n+1).

## Status

Currently working on Air quality part. TODO:
- Views and templates update.
- Map GIOS stations with OWM cities.
