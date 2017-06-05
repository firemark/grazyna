from grazyna.tests.commands.base import execute_message


def test_error(protocol):
    execute_message(protocol, ['ERROR'])
    assert protocol.messages == []
