from grazyna.utils import register
from grazyna import format
from grazyna.format import color
from datetime import timedelta, datetime, timezone

from aiohttp import request
import re

URL_API = 'http://api.openweathermap.org/data/2.5/forecast'
URL_API_LONG = URL_API + '/daily'

re_date = re.compile(r'([+-]?\d+)([dh])')

ICON_TO_UTF = {
    '01d': color('☀', color.yellow),
    '02d': color('☀', color.yellow),
    '03d': color('☁', color.white),
    '04d': color('☁', color.white),
    '09d': color('☔', color.light_blue),
    '10d': color('☔', color.light_blue),
    '11d': color('⚡', color.yellow),
    '13d': color('❄', color.white),
    '01n': color('☾', color.white),
    '02n': color('☾', color.white),
    '03n': color('☁', color.white),
    '04n': color('☁', color.white),
    '09n': color('☔', color.light_blue),
    '10n': color('☔', color.light_blue),
    '11n': color('⚡', color.yellow),
    '13n': color('❄', color.white),
}

@register(cmd='weather')
def weather(bot, city, day=None):
    dt = check_and_return_datetime(day)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

    delta_days = (dt - datetime.now()).days
    is_long_forecast = (delta_days > 5)
    if not is_long_forecast:
        response = yield from request('GET', URL_API, params={
            'q': city,
            'units': 'metric',
            'lang': 'pl',
            'APPID': bot.config.get('app_id'),
        })
    else:
        response = yield from request('GET', URL_API_LONG, params={
            'q': city,
            'units': 'metric',
            'lang': 'pl',
            'cnt': min(delta_days, 16),
            'APPID': bot.config.get('app_id'),
        })
    try:
        json_data = yield from response.json()
    finally:
        response.close()
    if json_data.get('cod') == 401:
        return
    data_list = json_data.get("list")
    if data_list is None:
        bot.reply('404 lol')
        return
    data = sorted(data_list, key=lambda x: abs(x['dt'] - timestamp))[0]
    try:
        weather = data['weather'][0]
    except IndexError:
        weather = {'description': '', 'icon': ''}

    if not is_long_forecast:
        temperature = data['main']['temp']
    else:
        if dt.hour < 6:
            period = 'night'
        elif dt.hour < 10:
            period = 'morn'
        elif dt.hour < 18:
            period = 'day'
        elif dt.hour < 22:
            period = 'eve'
        else:
            period = 'night'
        temperature = data['temp'][period]
    bot.reply('{city}: {temp} °C {icon} {desc}'.format(
        city=format.bold(city),
        temp=temperature,
        desc=weather['description'],
        icon=ICON_TO_UTF.get(weather['icon'], '')
    ))


def check_and_return_datetime(day):
    dt = datetime.now()
    if day is None:
        return dt

    dt_hour = datetime.now().replace(hour=12, minute=0, second=0)
    if day == "yesterday":
        return dt_hour - timedelta(days=1)
    if day == "tomorrow":
        return dt_hour + timedelta(days=1)

    match = re_date.match(day)
    if match is None:
        return dt
    number = int(match.group(1))
    if match.group(2) == 'd':
        return dt_hour + timedelta(days=number)
    else:
        return dt + timedelta(hours=number)
