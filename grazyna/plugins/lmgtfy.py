from grazyna.utils import register

from urllib.parse import quote


BASE_URL = 'http://lmgtfy.com/?q='


@register(cmd='lmgtfy')
def lmgtfy(bot, query):
    """let me google that for you"""

    url = BASE_URL + quote(query)
    bot.say(url)
