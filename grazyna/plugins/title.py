#!/usr/bin/python3

from ..utils import register
from .. import config
import re
import http.client
import requests
from requests.exceptions import RequestException
from html.parser import HTMLParser
from collections import defaultdict

default_charset = 'utf-8'

max_loop = 5
timeout = 2
max_bytes = 10240
re_charset = re.compile(r"^[^;]+; +charset=([\w\-]+)")
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
        elif tag == "meta":
            content = next((v for k, v in attrs if k == "content"), "")
            charset = re_charset.search(content)
            if charset:
                self.charset = charset.group(1)

    def handle_data(self, data):
        if self.title_tag:
            self.title = data

    def handle_endtag(self, tag):
        if tag == "title":
            self.title_tag = False

    @classmethod
    def get_title(cls, data):
        parser = cls()

        try:
            parser.feed(data)
        except:  #many bugs lol
            return None

        title = parser.title

        if title is None:
            return None

        title = title.strip()

        if title:
            return re_space.sub(' ', parser.unescape(title))


def get_response(adress, method='GET', data=None, headers=None, redirect=True,
                 ssl=False, session=None):
    headers = headers or {}

    if session is None:
        session = requests.Session()
        session.max_redirects = max_loop

    try:
        resp = session.request(
            method, adress, timeout=timeout, headers=headers,
            allow_redirects=redirect, verify=ssl, data=data)
    except RequestException:
        return None

    if resp.status_code != 200:
        return None

    raw = next(resp.iter_content(chunk_size=max_bytes))
    resp.msg = raw.decode(resp.encoding or default_charset,
                          errors='replace')
    resp.close()
    return resp



@register(reg=r'http(s?)://(\S+)|(www\.\S+)')
def title(bot, ssl: lambda s: s == 's', address, address_another):
    address = address or address_another

    if not address.startswith('http'):
        address = "http://" + address

    resp = get_response(address, ssl=ssl)

    if resp is None:
        return

    headers = resp.headers
    msg = resp.msg

    if "content-type" in headers:
        cont_type = headers["content-type"]
        # print(cont_type)

        if cont_type.startswith("text/html") and msg:
            title = TitleParser.get_title(msg)
            if title:
                bot.say(title)
