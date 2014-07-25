#!/usr/bin/python3
from ..utils import register
from .. import format


@register(cmd='help')
def help(bot, name):
    name = input.group(1)
    for module in modules.values():
        for reg, plugin in module:
            if plugin.help and name == plugin.name:
                bot.say(format.bold(plugin.name.upper()) + ': ' + plugin.help)
                return None
    bot.reply('Nie znalazłem takowego modułu.')


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