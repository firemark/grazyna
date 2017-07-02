from grazyna.plugins.quotes import quotes, get_replies
from grazyna.test_mocks.sender import SayMessage

from unittest.mock import patch
from asynctest.mock import patch as async_patch
from io import StringIO

import pytest


@pytest.mark.asyncio
@async_patch('grazyna.plugins.quotes.get_replies')
def test_quotes(get_replies_mock, public_bot):
    get_replies_mock.return_value = ['foobar']
    yield from quotes(public_bot)
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: foobar'),
    ]


@patch('grazyna.plugins.quotes.open', create=True)
def test_get_replies(open_mock, public_bot):
    public_bot.config['file'] = 'socek.txt'
    open_mock.return_value = StringIO(
        'foobar0\n'
        'foobar1\n'
    )
    data = ['foobar0', 'foobar1']

    for i in range(2):
        assert get_replies(public_bot) == data
    open_mock.assert_called_once_with('socek.txt')
    assert public_bot.temp['replies'] == data
