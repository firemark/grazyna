'''
Created on 31-03-2013

@author: firemark
'''
from asyncio import coroutine


class RequestBot(object):
    """First argument in register functions.
    Has useful informations as channel, nick
    and methods to communicate with user/channel"""

    __slots__ = ('private', 'user', 'chan', 'protocol', 'config', 'plugin',
                 'temp')

    def __init__(self, protocol, *, user=None, chan=None, private=False,
                 config=None, plugin=None, temp=None):
        self.protocol = protocol
        self.private = private
        self.user = user
        self.chan = chan
        self.config = config
        self.plugin = plugin
        self.temp = temp

    @coroutine
    def is_admin(self, nick=None):
        nick = nick or self.user.nick
        result = yield from self.protocol.whois(nick)
        return result.account in self.protocol.config.getlist('main', 'admins')

    @property
    def nick_chan(self):
        return self.user.nick if self.private else self.chan

    def say(self, msg, nick_chan=None):
        nick_chan = nick_chan or self.nick_chan
        self.protocol.say(nick_chan, msg)

    def notice(self, msg, nick=None):
        self.protocol.notice(nick or self.user.nick, msg)

    def reply(self, msg, chan=None, nick=None):
        self.protocol.reply(nick or self.user.nick, msg, chan or self.chan)

    def kick(self, who=None, why='', chan=None):
        if not self.private:
            self.protocol.kick(who or self.user.nick, chan or self.chan, why)

    def private_say(self, msg, nick=None):
        self.protocol.say(nick or self.user.nick, msg)

    def command(self, *args):
        self.protocol.send(*args)

    def command_msg(self, *args):
        self.protocol.send_msg(*args)

    def mode(self, flag, arg, chan=None):
        self.protocol.mode(chan or self.chan, flag, arg)

    def time_ban(self, time, who=None, why='', prefix=None, chan=None):
        chan = chan or self.chan
        prefix = prefix or "*!%s@%s" % (self.user.realname, self.user.host)
        who = who or self.user.nick
        self.protocol.time_ban(time, who, chan, why, prefix)
