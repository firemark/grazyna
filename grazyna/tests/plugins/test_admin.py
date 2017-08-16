import asyncio

from grazyna.plugins import admin as admin_plugins
from grazyna.irc.models import WhoisData
from grazyna.test_mocks.sender import SayMessage, Message

from asynctest.mock import patch as async_patch, Mock as AsyncMock
from io import StringIO

import pytest



@pytest.mark.asyncio
def test_admin_reload(public_bot):
    yield from admin_plugins.reload(public_bot, 'foobar')
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: Done!'),
    ]
    public_bot.protocol.importer.reload.assert_called_once_with('foobar')


@pytest.mark.asyncio
def test_admin_load(public_bot):
    yield from admin_plugins.load_plugin(public_bot, 'foobar', 'bar')
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: Done!'),
    ]
    public_bot.protocol.importer.load.assert_called_once_with('bar', 'foobar')


@pytest.mark.asyncio
def test_admin_remove(public_bot):
    yield from admin_plugins.remove_plugin(public_bot, 'foobar')
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: Done!'),
    ]
    public_bot.protocol.importer.remove.assert_called_once_with('foobar')


@pytest.mark.asyncio
def test_admin_kick_public(public_bot):
    yield from admin_plugins.kick(public_bot, who='socek', why='...')
    assert public_bot.protocol.messages == [
        Message('KICK', '#czarnobyl', 'socek', ':...'),
    ]


@pytest.mark.asyncio
def test_admin_kick_private(private_bot):
    yield from admin_plugins.kick(private_bot, who='socek', why='...')
    assert private_bot.protocol.messages == []


@pytest.mark.asyncio
def test_admin_join(public_bot):
    yield from admin_plugins.join(public_bot, chan='##python.pl')
    assert public_bot.protocol.messages == [
        Message('JOIN', '##python.pl'),
    ]


@pytest.mark.asyncio
def test_admin_eutanazja(public_bot):
    yield from admin_plugins.quit_bot(public_bot)
    assert public_bot.protocol.messages == [
        Message('QUIT', ':why? :('),
    ]


@pytest.mark.asyncio
def test_admin_say_public(public_bot):
    yield from admin_plugins.say(public_bot, 'foobar')
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'foobar')
    ]


@pytest.mark.asyncio
def test_admin_say_public_as_reply(public_bot):
    yield from admin_plugins.say(public_bot, 'bar', nick='foo', chan='#lol')
    assert public_bot.protocol.messages == [
        SayMessage('#lol', 'foo: bar')
    ]


@pytest.mark.asyncio
def test_admin_say_private(private_bot):
    yield from admin_plugins.say(private_bot, 'foobar')
    assert private_bot.protocol.messages == []


@pytest.mark.asyncio
def test_admin_op_public(public_bot):
    yield from admin_plugins.op(public_bot)
    assert public_bot.protocol.messages == [
        Message('MODE', '#czarnobyl', '+o', 'socek'),
    ]


@pytest.mark.asyncio
def test_admin_op_private(private_bot):
    yield from admin_plugins.op(private_bot)
    assert private_bot.protocol.messages == []


@pytest.mark.asyncio
def test_admin_part_public(public_bot):
    yield from admin_plugins.part(public_bot, why='...')
    assert public_bot.protocol.messages == [
        Message('PART', '#czarnobyl', ':...'),
    ]


@pytest.mark.asyncio
def test_admin_part_private(private_bot):
    yield from admin_plugins.part(private_bot)
    assert private_bot.protocol.messages == []


@pytest.mark.asyncio
@async_patch('grazyna.plugins.admin.open', create=True)
@async_patch('grazyna.plugins.admin.argv')
def test_admin_reload_config(mock_argv, mock_open, public_bot):
    mock_open.return_value = StringIO('''
[plugins]
ping = grazyna.plugins.ping
new_ping = grazyna.plugins.ping
    ''')
    importer = public_bot.protocol.importer
    importer.plugins = {
        'ping': None,
        'old_ping': None,
    }

    yield from admin_plugins.reload_config(public_bot)

    importer.remove.assert_called_once_with('old_ping')
    importer.load.assert_called_once_with('new_ping', 'grazyna.plugins.ping')
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: Done!'),
    ]


@pytest.mark.asyncio
@async_patch('grazyna.plugins.admin.open', create=True)
@async_patch('grazyna.plugins.admin.argv')
def test_admin_reload_config_without_plugins(mock_argv, mock_open, public_bot):
    mock_open.return_value = StringIO('''
[plugins]
ping = grazyna.plugins.ping
new_ping = grazyna.plugins.ping
    ''')
    yield from admin_plugins.reload_config(public_bot, 'no')

    importer = public_bot.protocol.importer
    assert importer.load.not_called
    assert importer.remove.not_called
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: Done!'),
    ]


@pytest.mark.asyncio
@async_patch('asyncio.sleep')
def test_admin_rocket(mock_sleep, public_bot):
    public_bot.config['__nick__'] = 'grazyna'

    @asyncio.coroutine
    def whois_func(enemy):
        whois_data  = WhoisData()
        whois_data.realname = 'foo'
        whois_data.host = 'bar'
        return  whois_data

    public_bot.protocol.whois = whois_func

    yield from admin_plugins.rocket(public_bot, 'socek', n=2)

    # 2 + 1 to wait for ban
    assert mock_sleep.call_count == 3
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', '2...'),
        SayMessage('#czarnobyl', '1...'),
        SayMessage('#czarnobyl', 'FIRE!'),
        Message('MODE', '#czarnobyl', '+b', '*!foo@bar'),
        Message('KICK', '#czarnobyl', 'socek', ':Kaboom!'),
    ]
