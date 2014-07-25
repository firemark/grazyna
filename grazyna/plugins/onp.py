#!/usr/bin/python3

from ..utils import create_help, register
from math import isnan
from random import random
from ..utils.types import range_int
from .. import format

operators = '-^+/*%&|=><~'


@register(cmd="onp")
def onp(bot, tasks, round:range_int(0)=3):
    score = calc(tasks.split(), round)
    bot.say("Wynik: %s" % score)


#@register(cmd='np')
def np(bot, tasks):
    tasks = tasks.split()
    new_tasks = []
    for task in tasks:
        try:
            num = float(task)
            new_tasks.append(num)
        except ValueError:
            new_tasks.append(task)
    new_tasks.reverse()
    score = calc(new_tasks)
    bot.say("Wynik: %s" % score)


def calc(tasks, round_num=3):
    buffor = []
    for task in tasks:
        try:
            num = float(task)
            buffor.append(num)
        except ValueError:
            for operator in task:
                if operator in operators:
                    if operator == '~':
                        try:
                            arg1 = buffor.pop()
                        except IndexError:
                            return "WTF"
                        arg1 = not bool(arg1)
                        buffor.append(arg1)
                        continue
                    try:
                        arg1 = buffor.pop()
                        arg2 = buffor.pop()
                    except IndexError:
                        return "WTF"
                    try:
                        if operator == '+':
                            arg2 += arg1
                        elif operator == '-':
                            arg2 -= arg1
                        elif operator == '/':
                            if arg1 != 0:
                                arg2 /= arg1
                            else:
                                arg2 = float('nan')
                        elif operator == '*':
                            arg2 *= arg1
                        elif operator == '%':
                            arg2 %= arg1
                        elif operator == '^':
                            if arg1 == 0:
                                arg2 = float('nan')
                            else:
                                arg2 = arg2 ** arg1
                        elif operator == '=':
                            arg2 = arg1 == arg2
                        elif operator == '>':
                            arg2 = arg1 > arg2
                        elif operator == '<':
                            arg2 = arg1 < arg2
                        elif operator == '&':
                            arg2 = bool(arg1) and bool(arg2)
                        elif operator == '|':
                            arg2 = bool(arg1) or bool(arg2)
                        else:
                            return "WTF"
                    except OverflowError:
                        return format.bold("Over 9000!!")

                    buffor.append(arg2)

    if  len(buffor) == 1:
        wart = buffor.pop()
        if type(wart) == bool:
            return wart.__repr__()
        else:
            if isnan(wart):
                if random() > 0.87:
                    return "NaNNaNNaNNaNNaN Batman!"
            return round(wart, round_num)
    else:
        return "WTF";
