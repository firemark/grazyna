from grazyna.plugins import admin as admin_plugins
from grazyna.test_mocks.sender import SayMessage, Message

from unittest.mock import patch
from asynctest.mock import patch as async_patch

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
