#!/usr/bin/python3
from ..utils import register
from .. import format

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
    bot.say(
        ', '.join(
            func.cmd.format(**importer.get_plugin_cfg(plugin.name))
            for plugin, func in importer.get_commands()
            if not func.admin_required
        )
    )


def show_command_help(bot, importer, name):
    plugin, func = importer.find_command(name)
    if func is None:
        return bot.reply('cmd not found')

    cmd = func.cmd.format(**importer.get_plugin_cfg(plugin.name))
    doc = re.sub('\s+', ' ', func.__doc__) if func.__doc__ else 'help not found'
    bot.say('{}: {}'.format(format.bold(cmd), doc))



#class commands(Plugin):
#    reg = r'^\.commands'
#    help = '.commands'
#    name = 'commands'
#
#    def use(self, input):
#        cmds = []
#        for module in modules.values():
#            cmds += [
#                      plugin.name
#                      for _, plugin in module
#                      if plugin.help
#                      ]
#            cmds.sort()
#        self.say(format.bold('commands: ') + ', '.join(cmds) )