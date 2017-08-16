from grazyna.utils import register
from grazyna.utils.types import range_int, is_chan
from grazyna.config import create_config

from sys import argv

import asyncio


@register(cmd='reload', admin_required=True)
def reload(bot, module):
    bot.protocol.importer.reload(module)
    bot.reply('Done!')


@register(cmd='load-plugin', admin_required=True)
def load_plugin(bot, module, name):
    bot.protocol.importer.load(name, module)
    bot.reply('Done!')


@register(cmd='remove-plugin', admin_required=True)
def remove_plugin(bot, name):
    bot.protocol.importer.remove(name)
    bot.reply('Done!')


@register(cmd='reload-config', admin_required=True)
def reload_config(bot, reload_plugins='yes'):
    with open(argv[1]) as f:
        bot.protocol.config = create_config(f)

    if reload_plugins != 'yes':
        bot.reply('Done!')
        return

    importer = bot.protocol.importer
    new_plugins = bot.protocol.config.items('plugins')
    loaded_plugins = set(importer.plugins.keys())
    plugins_to_remove = loaded_plugins - set(n for n, m in new_plugins)

    for name in plugins_to_remove:
        importer.remove(name)

    for name, module in bot.protocol.config.items('plugins'):
        if name not in loaded_plugins:
            bot.protocol.importer.load(name, module)

    bot.reply('Done!')


@register(cmd='kick', admin_required=True)
def kick(bot, who, chan=None, why=''):
    if bot.private and not chan:
        return
    bot.kick(who, why, chan)


@register(cmd='join', admin_required=True)
def join(bot, chan):
    bot.command('JOIN', chan)


@register(cmd='eutanazja', admin_required=True)
def quit_bot(bot):
    bot.command_msg('QUIT', 'why? :(')


@register(cmd='say', admin_required=True)
def say(bot, msg, nick=None, chan: is_chan=None):
    if bot.private and not (chan or nick):
        return

    if chan and nick:
        bot.say("{}: {}".format(nick, msg), chan)
    else:
        bot.say(msg, chan or nick)


@register(cmd='op', admin_required=True)
def op(bot, nick=None, chan: is_chan=None):
    if bot.private and not chan:
        return

    bot.mode("+o", nick or bot.user.nick, chan)


@register(cmd='part', admin_required=True)
def part(bot, chan: is_chan=None, why=None):
    if bot.private and not chan:
        return
    bot.command_msg('PART', chan or bot.chan, why)


@register(cmd='rocket', admin_required=True)
def rocket(bot, nick, n: range_int(0, 10)=3, chan: is_chan=None):
    if bot.private and not chan:
        return

    enemy = nick
    if n == 0 or enemy == bot.config['__nick__']:
        enemy = bot.user.nick

    for i in range(n):
        bot.say('{}...'.format(n - i))
        yield from asyncio.sleep(1)
    bot.say('FIRE!')
    whois = yield from bot.protocol.whois(enemy)
    yield from asyncio.sleep(1)
    prefix = "*!%s@%s" % (whois.realname or '*', whois.host or '*')
    bot.time_ban(n * 2, why='Kaboom!', who=enemy, chan=chan, prefix=prefix)
