import asyncio

from functools import wraps

from .. import log, config
from .exc import NoSuchNickError
from grazyna.modules import execute_msg_event
from .models import User


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

    __slots__ = ('user', 'data', 'protocol', 'command', 'prefix', 'importer')

    def __init__(self, protocol, data):
        self.protocol = protocol
        prefix_or_not = data[0]

        if prefix_or_not[0] == ':':
            self.prefix = prefix_or_not[1:]  # without ':'
            self.user = User(self.prefix)
            self.command = data[1]
        else:
            self.command = data[0]

        self.data = data

    def execute_message(self):
        command = self.command.lower()
        command = self.NUMERIC_COMMANDS.get(command, command)
        method = getattr(self, 'command_%s' % command, None)

        if method is not None:
            method()

    def get_from_whois(self, pop=False):
        nick = self.data[3]
        heap = self.protocol.whois_heap
        return heap.get(nick) if not pop else heap.pop(nick, None)

    def command_join(self):
        channel = self.data[2]
        log.write(channel, '%s(%s)::JOIN' % (self.user.nick, self.user.prefix))

    def command_ping(self):
        self.protocol.send('PONG', self.data[1])

    def command_part(self):
        channel = self.data[2]
        if len(self.data) == 4:
            reason = self.data[3]
            log.write(channel, "%s::PART[%s]" % (self.user.nick, reason))
        else:
            log.write(channel, "%s::PART" % self.user.nick)

    def command_kick(self):
        channel, nick = self.data[2:4]
        log.write(channel, "%s KICK %s" % (self.user.nick, nick))

        if nick == self.protocol.config['main']['nick']:
            self.protocol.send('JOIN', channel)

    def command_error(self):
        pass

    def command_privmsg(self):
        channel, text = self.data[2:]
        log.write(channel, "<%s> %s" % (self.user.nick, text))
        execute_msg_event(self.protocol, channel, self.user, text)

    def command_notice(self):
        self.command_privmsg()

    def command_start(self):
        if self.protocol.ready:
            return

        self.protocol.ready = True

        for channel in self.protocol.config['main']['channels']:
            self.protocol.send('JOIN', channel)

        self.protocol.config['main']['auth'].auth(self.protocol)

    @whois_command
    def command_whois_account(self, whois_data):
        whois_data.account = self.data[4]

    @whois_command
    def command_whois_user(self, whois_data):
        user, realname, host, _, ircname = self.data[3:5]
        whois_data.user = user
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