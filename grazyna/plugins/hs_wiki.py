from datetime import datetime
from aiohttp import ClientSession
from grazyna.utils import register
from grazyna.utils.types import range_int
from lxml.html import fromstring as fromstring_to_html

import asyncio
import dateparser

URL = 'https://wiki.hs-silesia.pl/wiki'
URL_MEETS = '%s/Planowane_spotkania' % URL
URL_CYCLIC = '%s/Cykliczne_obowiązki' % URL
TRASH_ID = "Wyw.C3.B3z_.C5.9Bmieci"
MEETS_ID = "Najbli.C5.BCsze_spotkania_tematyczne"
LIST_XPATH = '//span[starts-with(@id,$id)]/../following-sibling::ul/li'

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


def get_list_of_text_sorted_by_time(nodes, parse_date=None):
    parse_date = parse_date or (lambda text: dateparser.parse(text))
    now = datetime.now()
    list_data = sorted(
        ((text, date) for text, date in (
            (text.strip(), parse_date(text))
            for text in (node.text for node in nodes) if text
        ) if date is not None and date > now),
        key=lambda obj: obj[1] - now
    )
    return [text for text, date in list_data]


@register(cmd='next-meet')
def next_meet(bot, position: range_int(1)=1):
    html = yield from get_html(URL_MEETS)
    nodes = html.xpath(LIST_XPATH, id=MEETS_ID)
    list_data = get_list_of_text_sorted_by_time(
        nodes,
        lambda text: dateparser.parse(text.partition('-')[0].strip())
    )
    if not list_data:
        return bot.reply('¬_¬ no meetings')
    len_list = len(list_data)
    try:
        text = list_data[position - 1]
        text += " [%d meets]" % len_list
    except IndexError:
        text = 'only %d meets in calendar!' % len_list
    bot.reply(text)


@register(cmd='trash')
def trash(bot):
    html = yield from get_html(URL_CYCLIC)
    nodes = html.xpath(LIST_XPATH, id=TRASH_ID)
    list_data = get_list_of_text_sorted_by_time(nodes)
    if not list_data:
        return bot.reply('czysto i pięknie, uzupełnij wiki.')
    bot.reply(list_data[0])
