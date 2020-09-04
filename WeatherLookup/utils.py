import datetime
from matplotlib import pyplot as plt
from io import BytesIO
import base64


def unix_to_datetime(unix_date):
    """
    function for converting unix date format into datetime format
    :param unix_date: date presented in unix format
    :return: date in YYYY-mm-dd format
    """
    date = datetime.datetime.utcfromtimestamp(unix_date).strftime("%Y-%m-%d")
    return date


def unix_to_datetime_hour(unix_date):
    """
    function for converting unix date format into datetime format
    :param unix_date: date presented in unix format
    :return: date in dd-mm HH:MM format
    """
    date = datetime.datetime.utcfromtimestamp(unix_date).strftime("%d-%m %H:%M")
    return date


def get_plot_img(chart):
    buffer = BytesIO()
    chart.savefig(buffer, format='png', bbox_inches="tight")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic


def hourly_temperature_plot(api_data):
    date_x = api_data['date']
    temp_y = api_data['temp']

    fig = plt.figure(figsize=(12, 4))
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    plt.style.use('ggplot')
    axes.plot(date_x, temp_y, color='r', linewidth=2)

    plt.xlabel('Date and hour')
    plt.xticks(rotation=45)
    plt.locator_params(axis='x', nbins=4)

    plt.ylabel('Temperature (C)')
    plt.title('Hourly temperature forcast (48h)')
    plt.tight_layout()
    plt.grid(True)

    graphic = get_plot_img(plt)
    plt.close(fig)

    return graphic


def forecast_temperature_plot(df):
    fig = plt.figure(figsize=(12, 4))
    # get current axis
    axis = fig.gca()

    df.plot(kind='line', x='date', y='temp_day', color='red', ax=axis)
    df.plot(kind='line', x='date', y='temp_night', color='blue', ax=axis)

    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.ylabel('Temperature (C)')
    plt.title('Forecasted temperature')
    plt.grid(True)

    graphic = get_plot_img(plt)
    plt.close(fig)

    return graphic


def forecast_precipitation_plot(df):
    fig = plt.figure(figsize=(12, 4))
    # get current axis
    axis = fig.gca()

    df.plot(kind='bar', x='date', y='Rainfall', color='blue', ax=axis)
    df.plot(kind='bar', x='date', y='Snowfall', color='grey', ax=axis)
    ax3 = df['Chance of precipitation'].plot(secondary_y=True, color='r', x='date', linewidth=2, ax=axis)

    axis.set_xlabel('Date')
    xlabels = axis.get_xticklabels()
    axis.set_xticklabels(xlabels, rotation=45)

    axis.set_ylabel('Participation [mm/day/m2]')
    ax3.set_ylabel('Chance of Participation [%]')
    plt.title('Forecasted Participation')
    plt.grid(True)

    graphic = get_plot_img(plt)
    plt.close(fig)

    return graphic
