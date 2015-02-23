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


@register(cmd='czy')
def czy(bot, ask=None):
    replies = get_replies(bot.config)
    reply = random.choice(replies)
    bot.reply(reply)
czy.dict_replies = {}


def get_replies(config):
    plugin_name = config['__name__']
    replies = czy.dict_replies.get(plugin_name)
    if replies is None:
        pathname = config['file']
        with open(pathname) as f:
            replies = f.readlines()
        czy.dict_replies[plugin_name] = replies

@register(reg='[.?]czy.*')
def czy_reg(bot):
    czy(bot)
