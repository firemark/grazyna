from grazyna.tests.commands.base import execute_message
from grazyna.test_mocks.sender import protocol, Message


def test_kick(protocol):
    protocol.config = dict(main=dict(nick='firemark'))
    data = [':socek!a@b', 'KICK', '#czarnobyl', 'firemark']
    ctrl = execute_message(protocol, data)
    assert protocol.messages == [Message('JOIN', '#czarnobyl')]
    ctrl.log.assert_called_once_with('#czarnobyl', 'socek KICK firemark')

