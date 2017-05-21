from datetime import datetime

from grazyna.utils import register

@register(cmd='weekend')
def weekend(bot):
    """
    Answer to timeless question - are we at .weekend, yet?
    """
    current_date = datetime.now()
    day = current_date.weekday()
    nick = bot.user.nick
    if day in (5, 6):
        answer = "Oczywiście %s - jest weekend. Omawiamy tylko lajtowe tematy, ok?" % nick
    else:
        str_day = datetime.strftime(current_date, "%A")
        answer = "%s - dopiero %s, musisz jeszcze poczekać..." % (nick, str_day)

    bot.reply(answer)
