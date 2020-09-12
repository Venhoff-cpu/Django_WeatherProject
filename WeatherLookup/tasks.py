from Django_WeatherProject.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task(name='WeatherLookup.tasks.update_air_quality_db')
def update_air_quality_db():
    """
    Task running every hour getting data from GIOS API
    """
    from .api.gios_api_processor import get_all_stations, get_sensors, get_readings, get_air_index
    get_all_stations()
    logger.info("Stations updated")
    get_sensors()
    logger.info('Sensors updated')
    get_readings()
    logger.info('Readings updated')
    get_air_index()
    logger.info('Air indexes updated')
