from .models import WhoisFuture

import asyncio


class IrcSender(object):

    transport = None
    whois_heap = None

    def __init__(self):
        self.whois_heap = {}

    def send(self, *args):
        string = ' '.join(
            str(arg).replace('\r', '').replace('\n', '')
            for arg in args
        )[:510] + '\r\n'
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
        self.say(chan or nick, msg)

    def kick(self, nick, chan, why=''):
        self.send_msg('KICK', chan, nick, why or nick)

    def mode(self, chan, flag, arg):
        self.send('MODE', chan, flag, arg)

    @asyncio.coroutine
    def whois(self, nick):
        """

        :type nick: str
        :return: WhoisData
        """
        self.whois_heap[nick] = future = WhoisFuture()
        self.send('WHOIS', nick)
        result = yield from future
        return result

    def time_ban(self, time, nick, chan, why='', prefix=None):
        """

        :type time: int
        :type nick: str
        :type chan: str
        :type why: str
        :type prefix: str or NoneType
        """

        if time <= 0:
            return

        prefix = prefix or nick + '!*@*'
        self.mode(chan, '+b', prefix)
        self.kick(nick, chan, why)

        @asyncio.coroutine
        def timer():
            yield from asyncio.sleep(time)
            self.mode(chan, '-b', prefix)

        asyncio.async(timer())
