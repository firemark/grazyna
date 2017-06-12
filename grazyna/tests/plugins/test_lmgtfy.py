from grazyna.plugins.lmgtfy import lmgtfy
from grazyna.test_mocks.sender import SayMessage

import pytest


@pytest.mark.asyncio
def test_lmgtfy(public_bot):
    yield from lmgtfy(public_bot, 'socek klocek')
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'http://lmgtfy.com/?q=socek%20klocek'),
    ]

