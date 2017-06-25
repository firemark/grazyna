from grazyna.plugins.hs_wiki import next_meet, get_html, trash
from grazyna.test_mocks.sender import SayMessage

from asynctest import CoroutineMock, patch as async_patch
from lxml.html import fromstring, tostring
from freezegun import freeze_time
from unittest.mock import patch

import pytest
import asyncio


@pytest.mark.asyncio
@async_patch('grazyna.plugins.hs_wiki.ClientSession', autospec=True)
def test_get_html(session):
    get = session.return_value.get = CoroutineMock()
    resp = get.return_value
    raw_html = b'<html><body>socek</body></html>'
    resp.read.return_value = raw_html
    data = yield from get_html('http://www.socek.pl')
    assert raw_html == tostring(data)


@pytest.mark.asyncio
def test_next_meet(public_bot):

    @asyncio.coroutine
    def get_html(url):
        return fromstring('''
        <span id="Najbli.C5.BCsze_spotkania_tematyczne">lol title</span>
        <ul>
            <li>14 listopada 2015,9:00 - 15:00 Code retreat</li>
            <li>4 listopada 2015, 18:00 - MeetJS</li>
        </ul>
    ''') 
    with freeze_time('01-10-2015 12:00:00'),\
            patch('grazyna.plugins.hs_wiki.get_html', get_html):
        yield from next_meet(public_bot)
        yield from next_meet(public_bot, position=1)

    # position default(0): first newest
    # position 1: second newest
    public_bot.protocol.messages == [
        SayMessage(
            '#czarnobyl',
            'socek: 4 listopada 2015, 18:00 - MeetJS [2 meets]'
        ),
        SayMessage(
            '#czarnobyl',
            'socek: 14 listopada 2015,9:00 - 15:00 Code retreat [2 meets]'
        ),
    ]


@pytest.mark.asyncio
def test_next_meet_older_meets(public_bot):

    @asyncio.coroutine
    def get_html(url):
        return fromstring('''
            <h2>
                <span id="Najbli.C5.BCsze_spotkania_tematyczne">
                    lol title
                </span>
            </h2>
            <ul>
                <li>14 listopada 2015,9:00 - 15:00 Code retreat</li>
                <li>4 listopada 2015, 18:00 - MeetJS</li>
            </ul>
        ''') 
    with freeze_time('01-10-2016 12:00:00'),\
            patch('grazyna.plugins.hs_wiki.get_html', get_html):
        yield from next_meet(public_bot)

    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: ¬_¬ no meetings'),
    ]


@pytest.mark.asyncio
def test_next_meet_no_meets(public_bot):

    @asyncio.coroutine
    def get_html(url):
        return fromstring('''
            <h2>
                <span id="Najbli.C5.BCsze_spotkania_tematyczne">
                    lol title
                </span>
            </h2>
            <ul></ul>
        ''') 
    with freeze_time('01-10-2016 12:00:00'),\
            patch('grazyna.plugins.hs_wiki.get_html', get_html):
        yield from next_meet(public_bot)

    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: ¬_¬ no meetings'),
    ]


@pytest.mark.asyncio
def test_trash(public_bot):

    @asyncio.coroutine
    def get_html(url):
        return fromstring('''
            <h2>
                <span id="Wyw.C3.B3z_.C5.9Bmieci">lol title</span>
            </h2>
            <ul>
                <li>4 czerwca</li>
                <li>11 listopada</li>
            </ul>
        ''')

    with freeze_time('01-10-2016 12:00:00'),\
            patch('grazyna.plugins.hs_wiki.get_html', get_html):
        yield from trash(public_bot)

    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: 11 listopada'),
    ]


@pytest.mark.asyncio
def test_empty_trash(public_bot):

    @asyncio.coroutine
    def get_html(url):
        return fromstring('''
            <h2>
                <span id="Wyw.C3.B3z_.C5.9Bmieci">lol title</span>
            </h2>
            <ul></ul>
        ''')

    with freeze_time('01-10-2016 12:00:00'),\
            patch('grazyna.plugins.hs_wiki.get_html', get_html):
        yield from trash(public_bot)

    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: czysto i pięknie, uzupełnij wiki.'),
    ]
