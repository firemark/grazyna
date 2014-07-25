#!/usr/bin/python3

from ..utils import register
from .. import modules, irc, config
from time import sleep
from ..utils.types import range_int, is_chan

import sys


@register(cmd='reload', admin_required=True)
def reload(bot, module):
    modules.load_module(module)
    bot.reply('Done!')


@register(cmd='kick', admin_required=True)
def kick(bot, who, chan=None, why=''):
    if bot.private and not chan:
        return
    bot.kick(who, why, chan)


@register(cmd='join', admin_required=True)
def join(bot, chan):
    irc.send('JOIN', chan)


@register(cmd='eutanazja', admin_required=True)
def quit_bot(bot):
    irc.send_msg('QUIT', 'why? :(')


@register(cmd='say', admin_required=True)
def say(bot, msg, nick=None, chan:is_chan=None):
    if bot.private and not(chan or nick):
        return

    if chan and nick:
        bot.say(nick + ": " + msg, chan)
    else:
        bot.say(msg, chan or nick)

@register(cmd='op', admin_required=True)
def op(bot, nick=None, chan:is_chan=None):
    if bot.private and not chan:
        return

    bot.mode("+o", nick or bot.user.nick, chan)


@register(cmd='part', admin_required=True)
def part(bot, chan:is_chan, why=None):
    if bot.private and not chan:
        return
    irc.send_msg('PART', chan, why)


@register(cmd='rocket', admin_required=True)
def rocket(bot, nick, n:range_int(0, 10)=3, chan:is_chan=None):
    if bot.private and not chan:
        return

    enemy = nick
    if n == 0 or enemy == config.nick:
        enemy = bot.user.nick

    for i in range(n):
        bot.say(str(n - i) + '...')
        sleep(1)
    bot.say('FIRE!')
    sleep(1)
    bot.time_ban(n * 2, why='Kaboom!', who=enemy, chan=chan)
