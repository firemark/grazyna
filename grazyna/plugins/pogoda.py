#!/usr/bin/python3

'''
Created on 01-11-2012
Plugin ktory wyswietla pogode
Działa na api pogodynki

@author: firemark

'''

from ..utils import register, create_help
import http.client
from datetime import date as datetime_date
from datetime import timedelta, datetime
from urllib.parse import urlencode
from json import loads
from socket import timeout as TimeoutError
from ..utils.types import range_int

days = "przedwczoraj|wczoraj|teraz|dzisiaj|jutro|pojutrze|pon|wtr|sro|czw|pt|sob|nie"
weekdays = ("pon", "wtr", "sro", "czw", "pt", "sob", "nie")

url = "www.pogodynka.net"
adress = "/api:server/weather/getByDate.json?"
timeout = 10


@register(cmd='pogoda')
def pogoda(bot, city, day=None, hour: range_int(0, 24)=None):
    date = datetime_date.today()
    weekday = date.isoweekday()

    if not day or day == "dzisiaj" or day == "teraz":
        hour = hour or datetime.now().hour
    elif '-' in day:  # wykrywa date
        try:
            date = datetime_date(*[int(x) for x in day.split('-')][::-1])
            # po co parsowac po osobnych elementach
            # jak mozna generatorem!
        except ValueError:
            return None
    elif day == "przedwczoraj":
        date -= timedelta(days=2)
    elif day == "wczoraj":
        date -= timedelta(days=1)
    elif day == "jutro":
        date += timedelta(days=1)
    elif day == "pojutrze":
        date += timedelta(days=2)
    else:
        # dni tygodnia, od jutra do 'za tydzien'
        for i in range(1, 8):
            if weekdays[(weekday + i) % 7] == day:
                date += timedelta(days=i)
                break

    hour = hour or 12
    # polaczenie
    try:
        conn = http.client.HTTPConnection(url, timeout=timeout)
    except TimeoutError:
        pass
    else:
        conn.request("GET",
                     adress + urlencode({
                                        "date": date.strftime("%Y-%m-%d"),
                                        "city": city
                                        })
                     )
        try:
            response = conn.getresponse().read().decode('utf-8')
            weathers = loads(response)["response"]["weather"]["hourly"]
        except ValueError:
            pass
        except KeyError:
            pass
        except TypeError:
            pass
        else:
            obj = min(weathers,
                      key=lambda obj: abs(int(obj["time"]) - hour * 100))
            if city.lower() == "sosnowiec":
                bot.time_ban(3, why="Won!")
            bot.reply("Temp: {0} °C [odczuwalna {1} °C], "
                      "{2}, ciśnienie: {3} hPa".format(
                          obj["tempC"],
                          obj["FeelsLikeC"],
                          obj["weatherDesc"],
                          obj["pressure"]
                      )
                      )
        conn.close()
