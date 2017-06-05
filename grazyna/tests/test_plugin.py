from grazyna.modules import Plugin


def foo():
    pass


def test_plugin_init():
    plugin = Plugin('foobar', 'grazyna.foo', [foo])
    assert plugin.temp == {}
    assert plugin.name == 'foobar'
    assert plugin.module_path == 'grazyna.foo'
    assert plugin.config == {}
    assert plugin == [foo]


def test_plugin_repr():
    plugin = Plugin('foobar', 'grazyna.foo', [])
    assert repr(plugin) == "Plugin('foobar')"
