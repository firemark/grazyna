from grazyna.tests.commands.base import execute_message
from grazyna.test_mocks.sender import Message


def test_kick_bot(protocol):
    protocol.config['main']['nick'] = 'firemark'
    data = [':socek!a@b', 'KICK', '#czarnobyl', 'firemark']
    ctrl = execute_message(protocol, data)
    assert protocol.messages == [Message('JOIN', '#czarnobyl')]
    ctrl.log.assert_called_once_with('#czarnobyl', 'socek KICK firemark')


def test_kick_another_person(protocol):
    protocol.config['main']['nick'] = 'firemark'
    data = [':socek!a@b', 'KICK', '#czarnobyl', 'dimmur']
    ctrl = execute_message(protocol, data)
    assert protocol.messages == []
    ctrl.log.assert_called_once_with('#czarnobyl', 'socek KICK dimmur')
