import requests
import pandas as pd
from WeatherLookup.models import Stations, Sensors, Readings, AirIndex


def get_all_stations():
    r = requests.get('http://api.gios.gov.pl/pjp-api/rest/station/findAll')
    pd_stations = pd.json_normalize(r.json())
    for index, station in pd_stations.iterrows():
        _, created = Stations.objects.update_or_create(
            station_id=station["id"],
            address_street=station["addressStreet"],
            city_commune_communeName=station["city.commune.communeName"],
            city_commune_districtName=station["city.commune.districtName"],
            city_commune_provinceName=station["city.commune.provinceName"],
            station_city_id=station["city.id"],
            city_name=station["city.name"],
            gegrLat=station["gegrLat"],
            gegrLon=station["gegrLon"],
            station_name=station["stationName"],
        )


def get_sensors():
    for station in Stations.objects.values_list('station_id'):
        station_id = station[0]
        r = requests.get('http://api.gios.gov.pl/pjp-api/rest/station/sensors/'+str(station_id))
        sensors = pd.json_normalize(r.json())
        for index, sensor in sensors.iterrows():
            _, created = Sensors.objects.update_or_create(
                sensor_id=sensor["id"],
                param_id=sensor["param.idParam"],
                param_code=sensor["param.paramCode"],
                param_formula=sensor["param.paramFormula"],
                param_name=sensor["param.paramName"],
                station=Stations.objects.get(pk=station_id),
            )


def get_readings():
    for sensor in Sensors.objects.values_list('sensor_id'):
        sensor_id = sensor[0]
        r = requests.get('http://api.gios.gov.pl/pjp-api/rest/data/getData/'+str(sensor_id))
        readings = pd.json_normalize(r.json())

        readings_frame = pd.DataFrame()

        readings_frame['datetime'] = [d[u'date'] for d in readings["values"].values.item()]
        readings_frame['value'] = [d[u'value'] for d in readings["values"].values.item()]

        for index, reading in readings_frame.iterrows():
            _, created = Readings.objects.update_or_create(
                sensor=Sensors.objects.get(pk=sensor_id),
                datetime=reading['datetime'],
                value=reading['value'],
            )


def get_air_index():
    for station in Stations.objects.values_list('station_id'):
        station_id = station[0]
        r = requests.get('http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/'+str(station_id))
        air_indexes = pd.json_normalize(r.json())

        for index, air_index in air_indexes.iterrows():
            _, created = AirIndex.objects.update_or_create(
                station=Stations.objects.get(pk=station_id),
                index_date=air_index['stCalcDate'],
                index_levelID=air_index['stIndexLevel.id'],
                index_levelName=air_index['stIndexLevel.indexLevelName'],
            )
