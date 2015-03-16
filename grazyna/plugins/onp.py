#!/usr/bin/python3

from ..utils import create_help, register
from math import isnan
from random import random
from ..utils.types import range_int
from .. import format
import operator
import math

special_vars = {
    'pi': math.pi,
    'e': math.e
}

operator_funcs = {
    '+': operator.add,
    '-': operator.sub,
    '/': operator.truediv,
    '*': operator.mul,
    '%': operator.mod,
    '^': operator.pow,
    '=': operator.eq,
    '>': operator.gt,
    '<': operator.lt,
    '&': lambda a, b: bool(a) and bool(b),
    '|': lambda a, b: bool(a) or bool(b),
}

one_var_operator_funcs = {
    '~': lambda a: not bool(a),
    'sin': math.sin,
    'cos': math.cos,
    'log': math.log,
    'log10': math.log10,
    'log2': math.log2,
}


@register(cmd="onp")
def onp(bot, tasks, round:range_int(0)=3):
    """
        example: .onp 2 2 2 + * log2 round=5
        operators https://github.com/firemark/grazyna/blob/master/grazyna/plugins/onp.py
    """
    score = calc(tasks.split(), round)
    bot.say("Result: %s" % score)


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
        try:
            return special_vars[task]
        except KeyError:
            return None


def execute(op, buffer):
    func = operator_funcs.get(op)
    if func is None:
        func = one_var_operator_funcs.get(op)
        try:
            args = [buffer.pop()]
        except IndexError:
            return "WTF"
    else:
        try:
            args = [buffer.pop(), buffer.pop()]
        except IndexError:
            return "WTF"
    try:
        value = func(*args)
    except OverflowError:
        return format.bold("Over 9000!!")
    else:
        buffer.append(value)
