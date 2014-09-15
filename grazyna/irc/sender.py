import asyncio
from .models import WhoisFuture


class IrcSender(object):

    transport = None
    whois_heap = None

    def __init__(self):
        self.whois_heap = {}

    def send(self, *args):
        string = ' '.join(str(arg) for arg in args)[:510] + '\r\n'
        self.transport.write(string.encode())

    def send_msg(self, *args):
        """add ':' to last argument"""
        new_args = list(args)
        new_args[-1] = ':' + str(new_args[-1])
        self.send(*new_args)

    def say(self, nick_chan, msg):
        self.send_msg('PRIVMSG', nick_chan, msg)

    def notice(self, nick, msg):
        self.send_msg('NOTICE', nick, msg)

    def reply(self, nick, msg, chan=None):
        msg = msg if not chan else '%s: %s' % (nick, msg)
        self.say(nick, msg)

    def kick(self, nick, chan, why=''):
        self.send_msg('KICK', chan, nick, why)

    def mode(self, chan, flag, arg):
        self.send('MODE', chan, flag, arg)

    def whois(self, nick):
        self.whois_heap[nick] = future = WhoisFuture()
        data = yield from asyncio.wait(future)
        return data

    def time_ban(self, time, nick, chan, why='', prefix=None):
        prefix = prefix or nick + '!*@*'
        self.mode(chan, '+b', prefix)
        self.kick(nick, chan, why)

        if time > -1:
            Timer(time, lambda: self.mode(chan, '-b', prefix)).start()