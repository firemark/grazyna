#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
czy.py - odpowiada na pytanie
"""
import random
from config import czy_file
from ..utils import register, create_help
from ..irc import send
from threading import Timer
from time import sleep

create_help('czy', '?czy <pytanie>')

replies = []

with open(czy_file) as file_replies:
    replies = file_replies.readlines()


@register(cmd='czy')
def czy(bot, ask=None):
    reply = random.choice(replies)
    bot.reply(reply)
    if reply.endswith('wychodzę'):
        bot.command('part', bot.chan)
        sleep(2)
        Timer(10, lambda: send('join', bot.chan)).start()


@register(reg='[.?]czy.*')
def czy_reg(bot):
    czy(bot)
