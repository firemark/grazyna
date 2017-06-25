from grazyna.plugins.hs_wiki import next_meet, prev_meet, get_html, trash
from grazyna.test_mocks.sender import SayMessage

from asynctest import CoroutineMock, patch as async_patch
from lxml.html import fromstring, tostring
from freezegun import freeze_time

import pytest


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
@async_patch('grazyna.plugins.hs_wiki.get_html', autospec=True)
def test_next_meet(get_html, public_bot):
    get_html.return_value = fromstring('''
        <span id="Najbli.C5.BCsze_spotkania_tematyczne">lol title</span>
        <ul>
            <li>14 listopada 2015,9:00 - 15:00 Code retreat</li>
            <li>4 listopada 2015, 18:00 - MeetJS</li>
        </ul>
    ''') 
    with freeze_time('01-10-2015 12:00:00'):
        yield from next_meet(public_bot)
        yield from next_meet(public_bot, position=1)
    public_bot.protocol.messages == [
        SayMessage('socek: 4 listopada 2015, 18:00 - MeetJS [2 meets]'),
        SayMessage('socek: 14 listopada 2015,9:00 - 15:00 Code retreat [2 meets]'),
    ]
