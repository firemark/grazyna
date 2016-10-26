'''
Created on 01-04-2013

@author: firemark
'''
from grazyna.modules import get_args_from_text, check_type
from grazyna.utils.types import range_int

import unittest
import pytest

def func_test(bot, arg1, arg2,
              karg:range_int(0, 10)=0,
              akarg:int=2):
    pass
func_test.varkw = None
func_test.varargs = None
func_test.cmd = 'cmd'


@pytest.mark.parametrize('text,cor_args,cor_kwargs', [
    ("firemark tiramo", ["firemark", "tiramo"], {}),
    ("tiramo firemark with spaces", ["tiramo", "firemark with spaces"], {}),
    (
        "tiramo firemark with spaces karg= 2 akarg= 5",
        ["tiramo", "firemark with spaces"],
        {"karg": "2", "akarg": "5"}
    ), 
    (
        '"tiramo with spaces" firemark karg=" spaces "',
        ["tiramo with spaces", "firemark"],
        {"karg": " spaces "},
    ),
    (
        'karg= firemark arg2= 20 10 ',
        ["10"],
        {"karg": "firemark", "arg2": "20"}
    ),
])
def test__get_args(text, cor_args, cor_kwargs):
    max_args = 2
    args, kwargs = get_args_from_text(text, max_args)
    assert args == cor_args
    assert kwargs == cor_kwargs


@pytest.mark.parametrize('args,kwargs,result', [
    #without kwargs
    (["t1", "t2"], {}, {"arg1": "t1", "arg2": "t2", "karg": 0, "akarg": 2}),
    #with optionals
    (["t", "t", "-1", "-1"], {}, {"arg1": "t", "arg2": "t", "karg": 0, "akarg": -1}),
    (  # mixing
        ["ta", "t"], {"karg": "5", "akarg": "-1"},
        {"arg1": "ta", "arg2": "t", "karg": 5, "akarg": -1}
    ),
    (  # another
        ["t", "t"], {"karg": "15", "akarg": "10"},
        {"arg1": "t", "arg2": "t", "karg": 10, "akarg": 10}
    ),
    (  # without args
        [], {"arg1": "a", "arg2": "c", "karg": "5", "akarg": "10"},
        {"arg1": "a", "arg2": "c", "karg": 5, "akarg": 10}
    ),
])
def test__check_type(args, kwargs, result):
    assert check_type(args, kwargs, func_test) == result

