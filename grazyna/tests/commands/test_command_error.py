from grazyna.tests.commands.base import execute_message
from grazyna.test_mocks.sender import protocol


def test_error(protocol):
    execute_message(protocol, ['ERROR'])
    assert protocol.messages == []

