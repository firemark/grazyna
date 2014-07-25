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
time = 0
cell = 0
lastnick = ''
on_play = False
last_warn = datetime.now()

create_help('ruletka', '.krec || .strzal || .stats')


@register(cmd='krec', on_private=False)
def play(bot):
    global last_warn, cell, on_play
    if not on_play:
        on_play = True
        time = 0
        cell = randint(0, 5)
        last_warn = datetime.now()
        bot.say(format.bold('*trrrr*'))
    else:
        bot.say('zakrecone!')


@register(cmd='strzal', on_private=False)
def shot(bot):
    global last_warn, cell, on_play, stats, ban_times, lastnick, time
    if on_play:
            if lastnick == bot.user.prefix:
                if datetime.now() - last_warn < timedelta(minutes=5):
                    bot.reply('Spokoj!')
                    last_warn = datetime.now()
            else:
                last_warn = datetime.now()
                if cell == time:
                    bot.time_ban(ban_times[time], why='Bach!')
                    lastnick = ''
                    on_play = False
                else:
                    time += 1
                    lastnick = bot.user.prefix
                    bot.say(format.bold('*klik*'))
