from unittest.mock import Mock

from grazyna.utils import register, init_plugin
from grazyna.utils.event_loop import loop



mock_init_plugin = Mock()


@register(cmd='dummy')
def dummy(bot, a: str, b: int):
    pass


@register(reg=r'dum+y (a) (?P<b>b)')
def dummy_reg():
    pass


@register(cmd='dummier', private=True)
def dummy_private():
    pass


@loop('time', 0)
def dummy_loop():
    pass


inited_plugin = init_plugin(Mock())
