from datetime import datetime
from aiohttp import ClientSession
from grazyna.utils import register
from grazyna.utils.types import range_int
from lxml.html import fromstring as fromstring_to_html

import asyncio
import dateparser
import re

URL = 'https://wiki.hs-silesia.pl/wiki'
URL_MEETS = '%s/Planowane_spotkania' % URL
URL_CYCLIC = '%s/Cykliczne_obowiązki' % URL
TRASH_ID = "Wyw.C3.B3z_.C5.9Bmieci"
MEETS_ID = "Najbli.C5.BCsze_spotkania_tematyczne"
PREV_MEETS_ID = "Odbyte_spotkania"
LIST_XPATH = '//span[starts-with(@id,$id)]/../following-sibling::ul[1]/li'

re_date_range = re.compile(r"(\d\d+?)\s*-\s*(\d\d?)")
re_every = re.compile(r"^[Kk]a[żz]d[yaą]")


@asyncio.coroutine
def get_html(url):
    session = ClientSession()
    try:
        resp = yield from session.get(url)
        try:
            raw_data = yield from resp.read()
            data = raw_data.decode('utf-8', errors='xmlcharrefreplace')
            return fromstring_to_html(data)
        finally:
            resp.close()
    finally:
        session.close()


def get_list_of_text_sorted_by_time(nodes, parse_date=None):
    parse_date = parse_date or dateparser.parse
    now = datetime.now()
    texts = (node.text.strip() for node in nodes if node.text)
    texts_with_dates = ((text, parse_date(text)) for text in texts)

    list_data = sorted(
        (
            (text, date) for text, date in texts_with_dates
            if date is not None and date > now
        ),
        key=lambda obj: obj[1] - now
    )
    return [text for text, date in list_data]


def meet_parse_date(text):
    text = re_date_range.sub(r'\2', text)
    raw_date, _, _ = text.partition('-')
    raw_date = raw_date.strip()
    raw_date = re_every.sub('', raw_date)
    return dateparser.parse(raw_date)


@asyncio.coroutine
def show_meets(bot, position, label):
    html = yield from get_html(URL_MEETS)
    nodes = html.xpath(LIST_XPATH, id=label)
    list_data = get_list_of_text_sorted_by_time(nodes, meet_parse_date)
    if not list_data:
        return bot.reply('¬_¬ no meetings')
    len_list = len(list_data)
    try:
        text = list_data[position - 1]
        text += " [%d meets]" % len_list
    except IndexError:
        text = 'only %d meets in calendar!' % len_list
    bot.reply(text)


@register(cmd='next-meet')
def next_meet(bot, position: range_int(1)=1):
    yield from show_meets(bot, position, MEETS_ID)


@register(cmd='trash')
def trash(bot):
    html = yield from get_html(URL_CYCLIC)
    nodes = html.xpath(LIST_XPATH, id=TRASH_ID)
    list_data = get_list_of_text_sorted_by_time(nodes)
    if not list_data:
        return bot.reply('czysto i pięknie, uzupełnij wiki.')
    bot.reply(list_data[0])
