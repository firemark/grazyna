#!/usr/bin/python3
from grazyna.utils import register
from grazyna.models import Message
from grazyna import format

from inspect import getfullargspec
import re


@register(cmd='help')
def cmd_help(bot, name=None):
    """show help"""
    importer = bot.protocol.importer
    if name is None:
        show_commands(bot, importer)
    else:
        show_command_help(bot, importer, name)


@register(cmd='args')
def cmd_args(bot, name):
    """show args"""
    importer = bot.protocol.importer
    plugin, func = importer.find_command(name)
    if func is None:
        return bot.reply('cmd not found')
    cmd = func.cmd.format(**importer.get_plugin_cfg(plugin.name))
    argspec = getfullargspec(func)
    args = argspec.args[1:]
    defaults = argspec.defaults
    kwonlyargs = argspec.kwonlyargs
    bot.say(
        '{cmd}: {args} {optional} {very_optional}'.format(
            cmd=format.bold(cmd),
            args=' '.join(args[:-len(defaults)]),
            optional=' '.join('[%s]' % a for a in args[-len(defaults):]),
            very_optional=' '.join('[%s]' % a for a in kwonlyargs),
        )
    )


@register(cmd='source')
def source(bot):
    bot.say('https://github.com/firemark/grazyna')


def show_commands(bot, importer):
    private = bot.private
    commands = [
        func.cmd.format(**importer.get_plugin_cfg(plugin.name))
        for plugin, func in importer.get_commands(private=private)
        if not func.admin_required
        and importer.cmd_is_good(
            plugin, func,
            private=private,
            channel=bot.chan,
        )
    ]
    with bot.protocol.get_session() as session:
        commands += [msg.key for msg in (
            session.query(Message.key)
            .filter(Message.channel == bot.chan)
            .order_by(Message.key)
            .group_by(Message.key)
            .all()
        )]
    bot.say(', '.join(commands))


def show_command_help(bot, importer, name):
    plugin, func = importer.find_command(name)
    if func is None:
        return bot.reply('cmd not found')

    cmd = func.cmd.format(**importer.get_plugin_cfg(plugin.name))
    doc = re.sub('\s+', ' ', func.__doc__) if func.__doc__ else 'help not found'
    bot.say('{}: {}'.format(format.bold(cmd), doc))
