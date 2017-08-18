from unittest.mock import Mock, MagicMock
from asynctest.mock import CoroutineMock, patch as async_patch
from freezegun.api import freeze_time

from grazyna.irc.models import User
from grazyna.models import Message
from grazyna.modules import ModuleManager, Plugin, ExecutedCounter
from grazyna.request import RequestBot
from grazyna.test_mocks.sender import SayMessage
from grazyna.test_mocks.dummy_plugin import dummy

import pytest


@pytest.fixture
def manager(protocol):
    manager = ModuleManager(protocol)
    manager.config.add_section('plugins')
    manager.config.set('plugins', 'dummy', 'grazyna.test_mocks.dummy_plugin')
    return manager


@pytest.fixture
def manager_with_db(protocol_with_db):
    manager = ModuleManager(protocol_with_db)
    manager.config.add_section('plugins')
    manager.config.set('plugins', 'dummy', 'grazyna.test_mocks.dummy_plugin')
    return manager


@pytest.mark.asyncio
def test_load_all(manager: ModuleManager):
    yield from []  # noqa
    manager.load_all()

    plugin = manager.plugins['dummy']
    assert plugin.name == 'dummy'
    assert plugin.module_path == 'grazyna.test_mocks.dummy_plugin'
    assert plugin.config == {}

    from grazyna.test_mocks.dummy_plugin import (
        dummy, dummy_private, dummy_reg, inited_plugin
    )
    assert set(plugin) == {dummy, dummy_private, dummy_reg}
    inited_plugin.assert_called_once_with(plugin, manager.protocol)


@pytest.mark.asyncio
def test_load_all_with_config(manager: ModuleManager):
    yield from []  # noqa
    manager.config.add_section('plugin:dummy')
    manager.config.set('plugin:dummy', 'foo', 'bar')
    manager.load_all()

    plugin = manager.plugins['dummy']
    assert plugin.config == {'foo': 'bar'}


def test_cancel_tasks(manager: ModuleManager):
    manager.plugins['dummy'] = Plugin('a', 'b', [])
    manager.cancel_tasks()
    assert manager.plugins['dummy'].future.cancelled


def test_reload(manager: ModuleManager):
    manager.plugins['dummy'] = Plugin('a', 'path', [])
    manager.load = Mock()
    manager.reload('dummy')
    assert manager.plugins['dummy'].future.cancelled
    manager.load.called_once_with('dummy', 'path')


def test_remove(manager: ModuleManager):
    plugin = manager.plugins['dummy'] = Plugin('a', 'path', [])
    manager.load = Mock()
    manager.remove('dummy')
    assert plugin.future.cancelled
    assert manager.plugins == {}


@pytest.mark.asyncio
def test_execute_as_cmd(manager: ModuleManager):
    manager.execute_command = CoroutineMock()
    yield from manager.execute('#czarnobyl', User('a!b@c'), '.dummy lol 42')
    manager.execute_command.assert_called_once_with(
        'dummy', 'lol 42', False, '#czarnobyl', User('a!b@c'),
    )


@pytest.mark.asyncio
def test_execute_as_cmd_and_reply(manager: ModuleManager):
    manager.execute_command = CoroutineMock()
    yield from manager.execute('#czarnobyl', User('a!b@c'), 'bot: dummy lol')
    manager.execute_command.assert_called_once_with(
        'dummy', 'lol', False, '#czarnobyl', User('a!b@c'),
    )


@pytest.mark.asyncio
def test_execute_as_cmd_and_private(manager: ModuleManager):
    manager.execute_command = CoroutineMock()
    yield from manager.execute('socek', User('a!b@c'), '.dummy lol')
    manager.execute_command.assert_called_once_with(
        'dummy', 'lol', True, 'socek', User('a!b@c'),
    )


@pytest.mark.asyncio
def test_execute_as_reg(manager: ModuleManager):
    manager.execute_regs = CoroutineMock()
    yield from manager.execute('#czarnobyl', User('a!b@c'), 'dummmmmmy')
    manager.execute_regs.assert_called_once_with(
        'dummmmmmy', False, '#czarnobyl', User('a!b@c'),
    )


@pytest.mark.asyncio
def test_execute_command(manager: ModuleManager):
    manager.execute_func = CoroutineMock()
    manager.find_message_in_db = CoroutineMock()
    manager.load_all()
    yield from manager.execute_command(
        cmd='dummy',
        text='lol b=42',
        private=False,
        channel='#czarnobyl',
        user=User('a!b@c'),
    )

    assert not manager.find_message_in_db.called

    from grazyna.test_mocks.dummy_plugin import dummy
    manager.execute_func.assert_called_once_with(
        dummy,
        manager.plugins['dummy'],
        False,
        '#czarnobyl',
        User('a!b@c'),
        ['lol'],
        {'b': '42'},
    )


@pytest.mark.asyncio
def test_execute_not_exists_command(manager: ModuleManager):
    manager.execute_func = CoroutineMock()
    manager.find_message_in_db = CoroutineMock()
    manager.load_all()
    yield from manager.execute_command(
        cmd='szalona-dziewczyna',
        text='lol b=42',
        private=False,
        channel='#czarnobyl',
        user=User('a!b@c'),
    )

    assert not manager.execute_func.called

    manager.find_message_in_db.assert_called_once_with(
        'szalona-dziewczyna',
        '#czarnobyl',
        'lol b=42',
    )


@pytest.mark.asyncio
def test_execute_regs(manager: ModuleManager):
    manager.execute_func = CoroutineMock()
    manager.load_all()
    yield from manager.execute_regs(
        msg='dummmmy a b',
        private=False,
        channel='#czarnobyl',
        user=User('a!b@c'),
    )

    from grazyna.test_mocks.dummy_plugin import dummy_reg
    manager.execute_func.assert_called_once_with(
        dummy_reg,
        manager.plugins['dummy'],
        False,
        '#czarnobyl',
        User('a!b@c'),
        ('a', 'b'),
        {},
    )


@pytest.mark.asyncio
@async_patch('grazyna.modules.RequestBot')
def test_execute_func(bot_cls, manager: ModuleManager):
    manager.load_all()
    mock = MagicMock(spec=dummy, name='dummy')
    mock.__wrapped__ = dummy.__wrapped__
    bot = bot_cls.return_value = Mock(spec=RequestBot, name='bot')

    yield from manager.execute_func(
        func=mock,
        plugin=manager.plugins['dummy'],
        private=False,
        channel='#czarnobyl',
        user=User('a!b@c'),
        args=['lol'],
        kwargs={'b': '42'},
    )

    bot_cls.assert_called_once_with(
        protocol=manager.protocol,
        private=False,
        chan='#czarnobyl',
        config={'__nick__': 'bot'},
        plugin=manager.plugins['dummy'],
        user=User('a!b@c'),
        temp={},
    )

    mock.assert_called_once_with(bot, a='lol', b=42)


@pytest.mark.asyncio
def test_find_message_in_db(manager_with_db: ModuleManager):
    manager_with_db.load_all()
    with manager_with_db.protocol.get_session() as session:
        msg = Message()
        msg.channel = '#czarnobyl'
        msg.key = 'gjm'
        msg.message = '$0: $1gram juz miesiac; $@'
        session.add(msg)

    yield from manager_with_db.find_message_in_db(
        cmd='gjm',
        channel='#czarnobyl',
        text='lol kilo',
    )

    assert manager_with_db.protocol.messages == [
        SayMessage(
            '#czarnobyl',
            'lol: kilogram juz miesiac; lol kilo',
        )
    ]


def test_is_blocked(manager: ModuleManager):
    user = User('a!0@c')
    another_user = User('b!1@c')
    counters = manager.executed_counters
    with freeze_time('2017-01-01 12:00:00'):
        counter = ExecutedCounter()
        counter.counter = 50
        counters[user.prefix] = counter

    with freeze_time('2017-01-01 10:00:00'):
        counter = ExecutedCounter()
        counter.counter = 50
        counters[another_user.prefix] = counter

    with freeze_time('2017-01-01 12:00:00'):
        assert manager.is_blocked(user) is True
        assert manager.is_blocked(another_user) is False

    counters = manager.executed_counters
    assert counters[user.prefix].counter == 50
    assert counters[another_user.prefix].counter == 1
