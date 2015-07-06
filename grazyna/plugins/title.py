from ..utils import register

from aiohttp import ClientError, ClientSession, TCPConnector
from html.parser import HTMLParser, unescape

import asyncio
import re

default_charset = 'utf-8'

max_loop = 5
timeout = 2
max_bytes = 10240
re_charsets = (
    re.compile(rb"< *meta.+?charset=([\"']?)([\w\s\_-]+)\1[^>]*>"),
    re.compile(
        rb"< *meta.+?content=([\"']?)[^;]*; +charset=([\w\s\_-]+)\1[^>]*>"),
)
re_space = re.compile(r'\s+')


class TitleParser(HTMLParser):
    title_tag = False
    first = False
    title = None
    charset = "utf-8"

    def handle_starttag(self, tag, attrs):
        if self.first:
            return
        if tag == "title":
            self.title_tag = True
            self.first = True

    def handle_data(self, data):
        if self.title_tag:
            self.title = (self.title or '') + data

    def handle_endtag(self, tag):
        if tag == "title":
            self.title_tag = False

    @classmethod
    def get_title(cls, data):
        parser = cls(convert_charrefs=True)

        try:
            parser.feed(data)
        except:  #many bugs lol
            return None

        title = parser.title

        if title is None:
            return None

        title = title.strip()

        if title:
            return re_space.sub(' ', unescape(title))


@asyncio.coroutine
def get_response(address, headers=None, redirect=True,
                 ssl=False, session=None):

    if session is None:
        session = ClientSession(
            connector=TCPConnector(
                verify_ssl=ssl,
                conn_timeout=timeout
            )
        )
        session.max_redirects = max_loop

    try:
        resp = yield from session.get(
            address,
            #headers=headers,
            allow_redirects=redirect
        )
    except ClientError:
        return None, None

    if resp.status != 200:
        return None, None

    raw = yield from resp.content.read(max_bytes)
    charset = default_charset
    for re_charset in re_charsets:
        charset_match = re_charset.search(raw)
        if charset_match:
            charset = charset_match.group(2).decode()
            break

    try:
        msg = raw.decode(charset, errors='replace')
    except LookupError:
        return None, None

    resp.close()
    return msg, resp


@asyncio.coroutine
def check_title(bot, address, ssl):
    msg, resp = yield from get_response(address, ssl)

    if resp is None:
        return

    headers = resp.headers
    if "content-type" in headers:
        cont_type = headers["content-type"]
        if cont_type.startswith("text/html") and msg:
            title = TitleParser.get_title(msg)
            if title:
                bot.say("⚡ %s" % title)


@register(reg=r'http(s?)://(\S+)|(www\.\S+)')
def title(bot, ssl: lambda s: s == 's', address, address_another):
    address = address or address_another

    if not address.startswith('http'):
        address = "http://" + address

    asyncio.async(check_title(bot, address, ssl))
