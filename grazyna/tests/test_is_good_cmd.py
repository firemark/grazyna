from grazyna.modules import ModuleManager
from grazyna.irc.models import User, WhoisData
from unittest.mock import Mock, patch

import asyncio
import pytest


def create_func(cmd='test'):
    def func_test(bot, xx):
        pass
    func_test.varkw = None
    func_test.varargs = None
    func_test.cmd = cmd
    return func_test


def cmd_is_good(cfg, func, cmd=None, private=False, channel=None, user=None, whois=None):
    protocol = Mock(name='protocol')
    @asyncio.coroutine
    def whois_func(nick):
        return whois
    protocol.whois = whois_func
    plugin = Mock(name='plugin')
    plugin.name = 'test'
    mm = ModuleManager(protocol)
    mm.get_plugin_cfg = Mock(name='get_plugin_cfg', return_value=cfg)
    return mm.cmd_is_good(plugin, func, cmd, private, channel, user)


@pytest.mark.asyncio
def test__wrong_cmd():
    assert not (yield from cmd_is_good(
        cfg={},
        func=create_func(cmd='wrong_cmd'),
        cmd='correct_cmd',
    ))


@pytest.mark.asyncio
def test__wrong_formatted_cmd():
    assert not (yield from cmd_is_good(
        cfg={'foo': 'bar'},
        func=create_func(cmd='cmd_{foo}'),
        cmd='cmd_foo',
    ))


@pytest.mark.asyncio
def test__cmd_is_private():
    assert (yield from cmd_is_good(
        cfg={'foo': 'bar'},
        func=create_func(cmd='cmd_{foo}'),
        cmd='cmd_bar',
        private=True,
        channel=None,
    ))


@pytest.mark.asyncio
def test__channel_in_whitelist():
    assert (yield from cmd_is_good(
        cfg={'whitelist': '#bar,#foo'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#bar',
    ))


@pytest.mark.asyncio
def test__channel_not_in_whitelist():
    assert not (yield from cmd_is_good(
        cfg={'whitelist': '#bar,#foo'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#barfoo',
    ))


@pytest.mark.asyncio
def test__channel_in_blacklist():
    assert not (yield from cmd_is_good(
        cfg={'blacklist': '#bar,#foo'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#foo',
    ))


@pytest.mark.asyncio
def test__channel_not_in_blacklist():
    assert (yield from cmd_is_good(
        cfg={'blacklist': '#bar,#foo'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#barfoo',
    ))


@pytest.mark.asyncio
def test__user_and_channel_in_whitelist():
    whois = WhoisData()
    whois.account = 'FooNick'
    assert (yield from cmd_is_good(
        cfg={'whitelist': '#bar,#foobar{Barnick},#foo{FooNick;BarNick}'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#foo',
        user=User('foo!foo@foo'),
        whois=whois
    ))


@pytest.mark.asyncio
def test__user_in_whitelist():
    whois = WhoisData()
    whois.account = 'BarNick'
    assert (yield from cmd_is_good(
        cfg={'whitelist': '#foobar,#barfoo{FooNick},*{FooNick;BarNick}'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#bar',
        user=User('foo!foo@foo'),
        whois=whois,
    ))

@pytest.mark.asyncio
def test__user_and_channel_in_blacklist():
    whois = WhoisData()
    whois.account = 'BarNick'
    assert not (yield from cmd_is_good(
        cfg={'whitelist': '#foobar,#barfoo{BarNick},*{FooNick}'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#bar',
        user=User('foo!foo@foo'),
        whois=whois,
    ))
