from grazyna.plugins.ping import utf
from grazyna.test_mocks.sender import SayMessage

import pytest


@pytest.mark.asyncio
def test_utf(public_bot):
    yield from utf(public_bot)
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: żółw,lwiątko,kurczę'),
    ]
