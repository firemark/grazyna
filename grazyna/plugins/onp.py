#!/usr/bin/python3

from grazyna.utils import create_help, register
from grazyna.utils.types import range_int
from grazyna import format

from math import isnan
from random import random, randint
from collections import namedtuple
from functools import wraps

import operator
import math

special_vars = {
    'pi': math.pi,
    'e': math.e,
}

def reverse_func(func):
    @wraps(func)
    def inner(*args):
        return func(*args[::-1])
    return inner


operator_funcs = {
    #'op': (num, func),
    '+': (2, operator.add),
    '-': (2, operator.sub),
    '/': (2, operator.truediv),
    '//': (2, operator.floordiv),
    '%': (2, operator.mod),
    '*': (2, operator.mul),
    '**': (2, operator.pow),

    '=': (2, operator.eq),
    '>': (2, operator.gt),
    '<': (2, operator.lt),

    '&': (2, lambda a, b: bool(a) and bool(b)),
    '|': (2, lambda a, b: bool(a) or bool(b)),
    '^': (2, lambda a, b: bool(a) ^ bool(b)),

    '!': (1, lambda a: not bool(a)),
    '~': (1, lambda a: -a),

    '~-': (2, reverse_func(operator.sub)),
    '~/': (2, reverse_func(operator.truediv)),
    '~//': (2, reverse_func(operator.floordiv)),
    '~%': (2, reverse_func(operator.mod)),
    '~**': (2, reverse_func(operator.pow)),

    'sin': (1, math.sin),
    'cos': (1, math.cos),
    'log': (1, math.log),
    'tan': (1, math.tan),
    'log10': (1, math.log10),
    'log2': (1, math.log2),

    '?': (0, random),
    '??': (2, lambda a, b: randint(int(a), int(b))),
}


@register(cmd="onp")
def onp(bot, tasks, round:range_int(0)=3):
    """
        example: .onp 2 2 2 + * log2 round=5
        operators https://github.com/firemark/grazyna/blob/master/grazyna/plugins/onp.py
    """
    score = calc(tasks.split(), round)
    bot.say("Result: %s" % score)


@register(cmd="rpn")
def rpn(bot, tasks, round:range_int(0)=3):
    yield from onp(bot, tasks, round)


def calc(tasks, round_num=3):
    buffer = []
    for task in tasks:
        num = get_number(task)
        if num is None:
            result = execute(task, buffer)
            if result is not None:
                return result
        else:
            buffer.append(num)

    if len(buffer) > 0:
        value = buffer.pop()
        if type(value) == bool:
            return value.__repr__()
        else:
            if isnan(value):
                if random() > 0.87:
                    return "NaNNaNNaNNaNNaN Batman!"
            return round(value, round_num)
    else:
        return "WTF"


def get_number(task):
    try:
        return float(task)
    except ValueError:
        return special_vars.get(task)


def execute(op, buffer):
    try:
        len_args, func = operator_funcs[op]
    except KeyError:
        return 'WTF - %s is not a good operator' % op

    if len_args > 0:
        args = buffer[-len_args:]
        if len(args) != len_args:
            return "WTF"
        del buffer[-len_args:]
    else:
        args = []

    try:
        value = func(*args)
    except OverflowError:
        return format.bold("Over 9000!!")
    else:
        buffer.append(value)

