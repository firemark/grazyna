#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
ruletka ^_^
"""
from ..utils import register, create_help, init_plugin
from random import randint
from .. import format
from datetime import datetime, timedelta


ban_times = (5, 10, 13, 14, 15, 15)

create_help('ruletka', '.krec || .strzal')


@init_plugin
def init(plugin, protocol):
    plugin.temp.update(
        on_play=False,
        last_nick=None,
        last_warn=datetime.now()
    )


@register(cmd='krec', on_private=False)
def play(bot):
    if not bot.temp['on_play']:
        bot.temp.update(
            cell=0,
            cell_with_bullet=randint(0, 5),
            last_warn=datetime.now(),
            on_play=True,
        )
        bot.say(format.bold('*trrrr*'))
    else:
        bot.say('zakręcone!')


@register(cmd='strzal', on_private=False)
def shot(bot):
    if not bot.temp.get('on_play', False):
        return

    old_last_warn = bot.temp['last_warn']
    bot.temp['last_warn'] = datetime.now()

    if bot.temp['last_nick'] == bot.user.prefix:
        if datetime.now() - old_last_warn < timedelta(minutes=1):
            bot.reply('Spokoj!')
        return

    cell = bot.temp['cell']
    if bot.temp['cell_with_bullet'] == cell:
        bot.time_ban(ban_times[cell], why='Bach!')
        bot.temp.update(
            last_nick=None,
            on_play=False
        )
    else:
        bot.temp['cell'] += 1
        bot.temp['last_nick'] = bot.user.prefix
        bot.say(format.bold('*klik*'))
