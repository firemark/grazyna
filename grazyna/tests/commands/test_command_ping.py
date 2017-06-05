from grazyna.tests.commands.base import execute_message
from grazyna.test_mocks.sender import Message


def test_ping(protocol):
    execute_message(protocol, ['PING', 'foobar'])
    assert protocol.messages == [Message('PONG', 'foobar')]


def test_pong(protocol):
    execute_message(protocol, ['PONG', 'foobar'])
    assert protocol.messages == []
    assert protocol.ping_counter == 0
