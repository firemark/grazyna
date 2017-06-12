from grazyna.plugins.python import pep
from grazyna.test_mocks.sender import SayMessage

import pytest

@pytest.mark.asyncio
def test_pep(public_bot):
    yield from pep(public_bot, 8)
    public_bot.protocol.messages == [
        SayMessage(
            '#czarnobyl', 'socek: https://www.python.org/dev/peps/pep-0008'
        ),
    ]
