from grazyna.irc.message_controller import MessageController
from grazyna.test_mocks.sender import protocol


def test_init_without_data(protocol):
    ctrl = MessageController(protocol, [])
    assert ctrl.data == []


def test_init_with_prefix(protocol):
    data = [':Alex', 'PRIVMSG', 'Wiz', 'Hello World!']
    ctrl = MessageController(protocol, data)
    assert ctrl.data == data
    assert ctrl.command == 'PRIVMSG'


def test_init_without_prefix(protocol):
    data = ['PING', 'foo']
    ctrl = MessageController(protocol, data)
    assert ctrl.data == data
    assert ctrl.command == 'PING'


def test_execute_message_on_unknown_command(protocol):
    data = ['ROTFL']
    ctrl = MessageController(protocol, data)
    ctrl.execute_message()
    assert protocol.messages == []


def test_execute_message_without_data(protocol):
    data = []
    ctrl = MessageController(protocol, data)
    ctrl.execute_message()
    assert protocol.messages == []
