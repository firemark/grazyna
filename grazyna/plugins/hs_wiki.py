from datetime import datetime
from aiohttp import ClientSession
from grazyna.utils import register
from lxml.html import fromstring as fromstring_to_html

import asyncio
import dateparser

URL = 'https://wiki.hs-silesia.pl/wiki'
URL_MEETS = '%s/Planowane_spotkania' % URL
URL_CYCLIC = '%s/Cykliczne_obowiązki' % URL


@asyncio.coroutine
def get_html(url):
    session = ClientSession()
    try:
        resp = yield from session.get(url)
        try:
            raw_data = yield from resp.read()
            return fromstring_to_html(
                raw_data.decode('utf-8', errors='xmlcharrefreplace')
            )
        finally:
            resp.close()
    finally:
        session.close()


@register(cmd='next-meet')
def next_meet(bot, position: int=1):
    html = yield from get_html(URL_MEETS)
    now = datetime.now()
    list_data = sorted(
        (
            (text, date) for text, date in (
                (text.strip(), dateparser.parse(text.partition('-')[0].strip()))
                for text in (
                    node.text for node in
                    html.xpath("//ul[1]/li[position()>2]")
                )
                if text
            ) if date is not None and date > now
        ), key=lambda obj: abs(now - obj[1]).seconds
    )
    if not list_data:
        return bot.reply('¬_¬ no meetings')
    len_list = len(list_data)
    try:
        text, _ = list_data[position - 1]
        text += " [%d meets]" % len_list
    except IndexError:
        text = 'only %d meets in calendar!' % len_list
    bot.reply(text)
