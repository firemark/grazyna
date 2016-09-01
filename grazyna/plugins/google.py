from grazyna.utils import register
from grazyna import format

from aiohttp import request

GOOGLE_URL = 'https://ajax.googleapis.com/ajax/services/search/web'


@register(cmd='g')
def google(bot, query):
    """get first result of google query"""

    response = yield from request('GET', GOOGLE_URL, params={
        'q': query,
        'v': '1.0'
    })
    json_data = yield from response.json()
    data = json_data['responseData']
    if data is None:
        bot.reply(json_data['responseDetails'])
        return
    try:
        result = data['results'][0]
    except IndexError:
        bot.reply('not found')
        return

    title = result['titleNoFormatting']
    url = result['url']
    bot.say('{}: {}'.format(format.bold(title), url))
