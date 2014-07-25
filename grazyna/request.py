'''
Created on 31-03-2013

@author: firemark
'''
from .irc import *
from .threads import is_admin


class RequestBot(object):
    """First argument in register functions.
    Has useful informations as channel, nick
    and methods to comunicate with user/channel"""

    private = False
    user = None
    reason = None
    chan = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def is_admin(self, nick=None):
        return is_admin(nick or self.user.nick)

    def say(self, msg, nick_chan=None):
        say(
            nick_chan or (self.user.nick if self.private else self.chan),
            msg)

    def notice(self, msg, nick=None):
        notice(nick or self.user.nick, msg)

    def reply(self, msg, chan=None, nick=None):
        reply(nick or self.user.nick, msg, chan or self.chan)

    def kick(self, who=None, why='', chan=None):
        if not self.private:
            kick(who or self.user.nick, self.chan, why)

    def private(self, msg, nick=None):
        say(nick or self.user.nick, msg)

    def command(self, *args):
        send(*args)

    def mode(self, flag, arg, chan=None):
        mode(chan or self.chan, flag, arg)

    def time_ban(self, time, who=None, why='', prefix=None, chan=None):
        chan = chan or self.chan
        prefix = prefix or "*!%s@%s" % (self.user.realname, self.user.host)
        who = who or self.user.nick
        time_ban(time, who, chan, why, prefix)
