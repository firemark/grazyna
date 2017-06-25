from grazyna.plugins.onp import onp, rpn, calc
from grazyna import format
from grazyna.test_mocks.sender import SayMessage
from unittest.mock import patch
from math import isnan

import pytest


@pytest.mark.asyncio
def test_onp(public_bot):
    yield from onp(public_bot, '1234 1000 /', 2)
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'Result: 1.23'),
    ]


@pytest.mark.asyncio
def test_rpn(public_bot):
    yield from rpn(public_bot, '2 2 +', 2)
    assert public_bot.protocol.messages == [
        SayMessage('#czarnobyl', 'Result: 4.0'),
    ]

def str_calc(str_tasks):
    return calc(str_tasks.split())


def test_calc_priority():
    assert str_calc('2 2 2 * +') == 6


def test_calc_single_operator():
    assert str_calc('2 ~') == -2


def test_calc_wrong_operator():
    assert str_calc('2 SOCEK') == 'WTF - SOCEK is not a good operator'


def test_calc_reverse_operator():
    assert str_calc('2 0 ~-') == -2


def test_calc_empty_buffer():
    assert str_calc('') == 'WTF'


def test_calc_not_enought_buffer():
    assert str_calc('2 +') == 'WTF'


@patch('grazyna.plugins.onp.random')
def test_calc_batman(random):
    random.return_value = 0.88
    assert str_calc('nan') == 'NaNNaNNaNNaNNaN Batman!'


@patch('grazyna.plugins.onp.random')
def test_calc_nan_value(random):
    random.return_value = 0.0
    assert isnan(str_calc('nan'))


@patch('grazyna.plugins.onp.random')
def test_calc_zero_division(random):
    random.return_value = 0.0
    assert isnan(str_calc('0 0 /'))


def test_calc_bool():
    assert str_calc('1 1 =') is True


def test_overflow():
    assert str_calc('1024 1024 **') == format.bold('Over 9000!!')


@patch('grazyna.plugins.onp.operator_funcs', {'?': (0, lambda: 42)})
def test_calc_zero_arg_operator():
    assert str_calc('?') == 42
