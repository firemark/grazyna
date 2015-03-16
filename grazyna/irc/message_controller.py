import asyncio
from functools import wraps
from datetime import datetime
from asyncio import async

from .exc import NoSuchNickError
from .models import User

import os.path


def whois_command(func):

    @wraps(func)
    def inner(self):
        future = self.get_from_whois()
        if future:
            return func(self, future.data)

    return inner


class MessageController(object):

    NUMERIC_COMMANDS = {
        '005': 'start',
        '330': 'whois_account',  # I don't have idea where is in RFC
        '311': 'whois_user',
        '312': 'whois_server',
        '313': 'whois_operator',
        '319': 'whois_channels',
        '318': 'whois_end',
        '401': 'no_such_nick',
    }
    log_files = {}

    __slots__ = ('user', 'data', 'protocol', 'command', 'prefix')

    def __init__(self, protocol, data):
        self.protocol = protocol
        if not data:
            self.data = []
            return
        prefix_or_not = data[0]

        if prefix_or_not[0] == ':':
            self.prefix = prefix_or_not[1:]  # without ':'
            self.user = User(self.prefix)
            self.command = data[1]
        else:
            self.command = data[0]

        self.data = data

    @property
    def config(self):
        return self.protocol.config

    def execute_message(self):
        if not self.data:
            return
        command = self.command.lower()
        command = self.NUMERIC_COMMANDS.get(command, command)
        method = getattr(self, 'command_%s' % command, None)

        if method is not None:
            method()

    def get_from_whois(self, pop=False):
        nick = self.data[3]
        heap = self.protocol.whois_heap
        return heap.get(nick) if not pop else heap.pop(nick, None)

    def log(self, channel, msg):
        str_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if channel not in self.log_files:
            self.log_files[channel] = open(
                os.path.join(self.config.get('main', 'dir_log'), channel), "at"
            )
        file_log = self.log_files[channel]
        file_log.write('[%s] %s\r\n"' % (str_datetime, msg))
        file_log.flush()

    def command_join(self):
        channel = self.data[2]
        self.log(channel, '%s(%s)::JOIN' % (self.user.nick, self.user.prefix))

    def command_ping(self):
        self.protocol.send('PONG', self.data[1])

    def command_pong(self):
        self.protocol.ping_counter = 0

    def command_part(self):
        channel = self.data[2]
        if len(self.data) == 4:
            reason = self.data[3]
            self.log(channel, "%s::PART[%s]" % (self.user.nick, reason))
        else:
            self.log(channel, "%s::PART" % self.user.nick)

    def command_kick(self):
        channel, nick = self.data[2:4]
        self.log(channel, "%s KICK %s" % (self.user.nick, nick))

        if nick == self.protocol.config['main']['nick']:
            self.protocol.send('JOIN', channel)

    def command_error(self):
        pass

    def command_privmsg(self):
        channel, text = self.data[2:]
        self.log(channel, "<%s> %s" % (self.user.nick, text))
        async(self.protocol.importer.execute(channel, self.user, text))

    def command_notice(self):
        self.command_privmsg()

    def command_start(self):
        if self.protocol.ready:
            return

        self.protocol.ready = True
        async(ping_pong(self.protocol))

        for channel in self.protocol.config.getlist('main', 'channels'):
            self.protocol.send('JOIN', channel)

        kwargs = dict(self.protocol.config.items('auth'))
        del kwargs['module']
        cls_auther = self.protocol.config.getmodule('auth', 'module')
        cls_auther(**kwargs).auth(self.protocol)

    @whois_command
    def command_whois_account(self, whois_data):
        whois_data.account = self.data[4]

    @whois_command
    def command_whois_user(self, whois_data):
        nick, realname, host, _, ircname = self.data[3:8]
        whois_data.nick = nick
        whois_data.host = host
        whois_data.realname = realname
        whois_data.ircname = ircname

    @whois_command
    def command_whois_server(self, whois_data):
        whois_data.server = self.data[2]

    @whois_command
    def command_whois_channels(self, whois_data):
        whois_data.channels = [
            channel.strip('@%+') for channel in self.data[2].split()
        ]

    def command_whois_end(self):
        future = self.get_from_whois(pop=True)
        if future:
            future.set_result(future.data)

    def command_no_nick(self):
        future = self.get_from_whois(pop=True)
        if future:
            future.set_exception(NoSuchNickError)


@asyncio.coroutine
def ping_pong(protocol):
    while True:
        protocol.ping_counter += 1
        protocol.send_msg('PING', '1337')
        yield from asyncio.sleep(64)
        if protocol.ping_counter > 4:  # 4 * 64 = 256 seconds
            break
    protocol.transport.close()
