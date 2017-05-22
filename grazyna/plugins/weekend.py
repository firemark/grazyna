"""Answer to timeless question - are we at .weekend, yet?"""
from datetime import datetime

from grazyna.utils import register

@register(cmd='weekend')
def weekend(bot):
    """Answer to timeless question - are we at .weekend, yet?"""
    current_date = datetime.now()
    day = current_date.weekday()
    if day in (5, 6):
        answer = "Tak, u mnie jest weekend. Omawiamy tylko lajtowe tematy, ok?"
    else:
        answer = "Niestety dopiero {day}, musisz jeszcze poczekać..."\
                 .format(day=datetime.strftime(current_date, "%A"),)
    bot.reply(answer)
