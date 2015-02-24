#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
czy.py - odpowiada na pytanie
"""
import random
from ..utils import register, create_help
from threading import Timer
from time import sleep

create_help('czy', '?czy <pytanie>')


@register(cmd='czy')  # BotArg('alias')
def czy(bot, ask=None):
    replies = get_replies(bot)
    reply = random.choice(replies)
    bot.reply(reply)


def get_replies(bot):
    plugin_name = bot.config['__name__']
    replies = bot.temp.get('replies')
    if replies is None:
        pathname = bot.config['file']
        with open(pathname) as f:
            replies = f.readlines()
        bot.temp['replies'] = replies

@register(reg='[.?]czy.*')
def czy_reg(bot):
    czy(bot)
