from grazyna.tests.commands.base import execute_message
from grazyna.test_mocks.sender import protocol, Message

import pytest

data = [':irc.server.net', '005', 'firemark', 'CHANTYPES=#', 'NICKLEN=30'] 


def test_start_if_is_started(protocol):
    protocol.ready = True
    ctrl = execute_message(protocol, data)
    assert protocol.messages == []


@pytest.mark.asyncio
def test_start_if_is_not_started(protocol):
    yield from []  # noqa - turn on global event_loop
    protocol.ready = False
    protocol.config['main']['channels'] = '#foo, #baar'
    ctrl = execute_message(protocol, data)
    assert protocol.ready is True
    assert protocol.messages == [
        Message('JOIN', '#foo'),
        Message('JOIN', '#baar'),
    ]
