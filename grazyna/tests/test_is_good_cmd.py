from grazyna.modules import ModuleManager
from unittest.mock import Mock, patch


def create_func(cmd='test'):
    def func_test(bot, xx):
        pass
    func_test.varkw = None
    func_test.varargs = None
    func_test.cmd = cmd
    return func_test


def cmd_is_good(cfg, func, cmd=None, private=False, channel=None, user=None):
    protocol = Mock(name='protocol')
    plugin = Mock(name='plugin')
    plugin.name = 'test'
    mm = ModuleManager(protocol)
    mm.get_plugin_cfg = Mock(name='get_plugin_cfg', return_value=cfg)
    return mm.cmd_is_good(plugin, func, cmd, private, channel, user)


def test__wrong_cmd():
    assert not cmd_is_good(
        cfg={},
        func=create_func(cmd='wrong_cmd'),
        cmd='correct_cmd',
    )


def test__wrong_formatted_cmd():
    assert not cmd_is_good(
        cfg={'foo': 'bar'},
        func=create_func(cmd='cmd_{foo}'),
        cmd='cmd_foo',
    )


def test__cmd_is_private():
    assert cmd_is_good(
        cfg={'foo': 'bar'},
        func=create_func(cmd='cmd_{foo}'),
        cmd='cmd_bar',
        private=True,
        channel=None,
    )


def test__channel_in_whitelist():
    assert cmd_is_good(
        cfg={'whitelist': '#bar,#foo'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#bar',
    )


def test__channel_not_in_whitelist():
    assert not cmd_is_good(
        cfg={'whitelist': 'bar,foo'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#barfoo',
    )


def test__channel_in_blacklist():
    assert not cmd_is_good(
        cfg={'blacklist': '#bar,#foo'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#foo',
    )


def test__channel_not_in_blacklist():
    assert cmd_is_good(
        cfg={'blacklist': '#bar,#foo'},
        func=create_func(cmd='cmd'),
        cmd='cmd',
        channel='#barfoo',
    )

