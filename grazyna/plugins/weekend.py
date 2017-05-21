from datetime import datetime

from grazyna.utils import register

@register(cmd='weekend')
def weekend(bot):
    """
    Answer to timeless question - are we at .weekend, yet?
    """
    current_date = datetime.now()
    day = current_date.weekday()
    answer = "WTF?"
    if day in (5, 6):
        answer = "Oczywiście %s - jest weekend. Omawiamy tylko lajtowe tematy, ok?" % bot.nick
    else:
        answer = "%s - dopiero %s, musisz jeszcze poczekać..." % (bot.nick, datetime.strftime(current_date, "%A"))

    bot.reply(answer)
