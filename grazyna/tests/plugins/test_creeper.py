from grazyna.plugins.creeper import creeper
from grazyna.test_mocks.sender import Message

import pytest
import re


@pytest.mark.asyncio
def test_creeper(public_bot):
    yield from creeper(public_bot)
    assert public_bot.protocol.messages == [
        Message('KICK', '#czarnobyl', 'socek', ':Alert!'),
    ]


def test_creeper_regexp():
    assert re.match(creeper.reg, 'ssss!')
