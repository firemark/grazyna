#!/usr/bin/python3

#from plugin import Plugin
from .. import config
import random
from ..utils import register

"""
@register(reg=r'^' + config.nick + r'!$')
def ping(bot):
    bot.say(bot.user.nick + '!')


@register(reg=r'(?i)^' + config.nick + r': +(?:(?:Cze[sś][cć])|(?:Siema(?:sz)?)|(?:He[jy])|(?:!+))[!.]? *$')
def ping2(bot):
    bot.reply(random.choice((
                'Hey', 'Siema', '?', 'czeeeść'
                                )))

"""
@register(cmd='utf8')
def utf(bot):
    """show utf-8 chars"""
    bot.reply("żółw,lwiątko,kurczę")
