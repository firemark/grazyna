from grazyna.irc.message_controller import MessageController, ping_pong
from unittest.mock import patch
from freezegun import freeze_time
from io import StringIO

import pytest
import asynctest


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


@patch('builtins.open')
def test_log(open_mock, protocol):
    stream = open_mock.return_value = StringIO()
    protocol.config['main']['dir_log'] = '/foo'
    ctrl = MessageController(protocol, [])
    with freeze_time('2017-06-06 06:06:06'):
        ctrl.log('#czarnobyl', 'foobar msg')
        ctrl.log('#czarnobyl', 'another msg')
    open_mock.assert_called_once_with('/foo/#czarnobyl', 'at')
    assert stream.getvalue() == (
        '[06-06-2017 06:06:06] foobar msg\r\n'
        '[06-06-2017 06:06:06] another msg\r\n'
    )


@pytest.mark.asyncio
@asynctest.mock.patch('grazyna.irc.message_controller.asyncio')
def test_ping_pong(asyncio_mock, protocol):
    yield from ping_pong(protocol)
    asyncio_mock.sleep.assert_called_with(64)
    assert asyncio_mock.sleep.call_count == 5
    assert protocol.ping_counter == 5
    protocol.transport.close.assert_called_once_with()
