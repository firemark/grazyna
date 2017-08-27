"""
to setup this please visit
https://developers.google.com/custom-search/json-api/v1/using_rest
"""
from grazyna.utils import register
from grazyna import format

from aiohttp import request

GOOGLE_URL = 'https://www.googleapis.com/customsearch/v1'


@register(cmd='g')
def google(bot, query):
    """get first result of google query"""

    params = dict(
        key=bot.config['key'],
        cx=bot.config['cx'],
        prettyPrint=False,
        q=query,
    )
    response = yield from request('GET', GOOGLE_URL, params=params)
    json_data = yield from response.json()
    error = json_data.get('error')
    if error:
        bot.say('err: %s' % error['message'])
    items = json_data.get('items', [])

    try:
        result = items[0]
    except IndexError:
        bot.reply('not found')
        return

    title = result['title']
    url = result['link']
    bot.say('{}: {}'.format(format.bold(title[:50]), url))
