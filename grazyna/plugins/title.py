# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import asyncio
import re
import string
from html.parser import HTMLParser, unescape
from io import BytesIO
from random import choice

from aiohttp import ClientError, ClientSession, TCPConnector

from ..utils import register


default_charset = 'utf-8'

TIMEOUT = 2
MAX_CHUNK_BYTES = 1024
MAX_CHUNKS = 8
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
        except:  # many bugs lol
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
    """
    :return: tuple of message and response
    :rtype: (string, aiohttp.Request)
    """
    try:
        if session is None:
            session = ClientSession(
                connector=TCPConnector(
                    verify_ssl=ssl,
                    conn_timeout=TIMEOUT
                )
            )
        resp = yield from session.get(
            address,
            headers=headers,
            allow_redirects=redirect
        )
        try:
            if resp.status != 200:
                return None, None
            raw_io = BytesIO()
            for _ in range(MAX_CHUNKS):
                chunk = yield from resp.content.read(MAX_CHUNK_BYTES)
                if not chunk:
                    break
                raw_io.write(chunk)
            raw = raw_io.getvalue()
        finally:
            resp.close()
    except ClientError:
        return None, None
    finally:
        session.close()

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
    return msg, resp


def address_in_blacklist(address, blacklist):
    for entry in blacklist:
        if address.startswith(entry):
            return True


@asyncio.coroutine
def check_title(bot, address, ssl):
    if address_in_blacklist(address, bot.config.values()):
        return

    msg, resp = yield from get_response(address, ssl=ssl)

    if resp is None:
        return

    headers = resp.headers
    if "content-type" not in headers:
        return
    cont_type = headers["content-type"]
    if not cont_type.startswith("text/html"):
        return
    if not msg:
        return

    title = TitleParser.get_title(msg)

    if not title:
        return
    if title.startswith('Rick Astley'):
        title = 'Funny %s - YouTube' % choice((
            'cats', 'dogs', 'firemark'
        ))
    bot.say("⚡ %s" % title)


@register(reg=r'http(s?)://(\S+)|(www\.\S+)')
def title(bot, ssl: lambda s: s == 's', address, address_another):
    address = address or address_another

    # ensure that characters like \x01 are removed
    address = "".join([char for char in address if char in string.printable])
    if not address.startswith('http'):
        address = "http://" + address

    yield from check_title(bot, address, ssl)
