#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
ruletka ^_^
"""
from ..utils import register, create_help
from random import randint
from ..irc import send
from .. import format
import json
from datetime import datetime, timedelta


ban_times = (5, 10, 13, 14, 15, 15)

create_help('ruletka', '.krec || .strzal || .stats')

@register(cmd='krec', on_private=False)
def play(bot):
    if not bot.temp.get('on_play', False):
        on_play = True
        bot.temp['cell'] = 0
        bot.temp['cell_with_bullet'] = randint(0, 5)
        bot.temp['last_warn'] = datetime.now()
        bot.say(format.bold('*trrrr*'))
    else:
        bot.say('zakręcone!')


@register(cmd='strzal', on_private=False)
def shot(bot):
    if not bot.temp.get('on_play', False):
        return

    old_last_warn = bot.temp.get('last_warn', datetime.now())
    bot.temp['last_warn'] = datetime.now()

    if bot.temp.get('last_nick') == bot.user.prefix:
        if datetime.now() - old_last_warn < timedelta(minutes=5):
            bot.reply('Spokoj!')
        return

    cell = bot.temp['cell']
    if bot.temp['cell_with_bullet'] == cell:
        bot.time_ban(ban_times[cell], why='Bach!')
        del bot.temp['last_nick']
        bot.temp['on_play'] = False
    else:
        bot.temp['cell'] += 1
        bot.temp['last_nick'] = bot.user.prefix
        bot.say(format.bold('*klik*'))
