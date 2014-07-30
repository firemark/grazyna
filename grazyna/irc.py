#!/usr/bin/python3

import socket, config
import config
import asyncio
from threading import Timer

s = ''
ready = False


class IrcClient(asyncio.Protocol):

    ready = False

    def connection_made(self, transport):
        pass

    def data_received(self, raw_messages):
        for message in self._parse_raw_messages_generator(raw_messages):
            if config.debug:
                print(' '.join(message))
            if message[0] == 'PING':
                self.transport.send('PONG', message[1])
            else:
                MessageController(message).execute_message()

    def connection_lost(self, exc):
        asyncio.get_event_loop().stop()

    @classmethod
    def _parse_raw_messages(cls, raw_messages):
        gen = cls._parse_raw_messages_generator(raw_messages)
        return (msg for msg in gen if len(msg) >= 2)

    @staticmethod
    def _parse_raw_messages_generator(raw_messages):
        for codec in config.codec:
            try:
                encoded_data = raw_messages.decode(codec).split('\r\n')
            except:
                continue
            else:
                break
        else:
            return

        for raw_message in filter(encoded_data, lambda x: x):
            if raw_message[0] == ':':
                raw_message = raw_message[1:]

            if ':' in raw_message:
                left_message, right_message = cmd.split(":", 1)
                yield left_message.split() + [right_message]
            else:
                yield raw_message.split()

    def send(*args):
        string = ' '.join(str(arg) for arg in args)[:512] + '\r\n'
        self.transport.send(string.encode())        

def connect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((config.host, config.port))
        print("CONN>>", config.host, ":", str(config.port))
    except socket.error as e:
        print("ERR>>", e)

    nick = config.nick
    data = ''
    send('PASS', config.password)
    send('NICK', nick)
    send_msg('USER', config.realname, 'wr', '*', config.ircname)



def send_msg(*args):
    """add ':' to last argument"""
    new_args = list(args)
    new_args[-1] = ':' + str(new_args[-1])
    send(*new_args)


def close():
    global s
    s.close()


class User(object):
    """User class - has nick, realname, and host"""
    nick = ""
    host = ""
    realname = ""

    def __init__(self, prefix=None):
        try:
            self.nick, name_host = prefix.split('!')
            self.realname, self.host = name_host.split('@')
        except:
            pass

    @property
    def prefix(self):
        return "%s@%s" % (self.realname, self.host)

#Useful functions


def say(nick_chan, msg):
    send_msg('PRIVMSG', nick_chan, msg)


def notice(nick, msg):
    send_msg('NOTICE', nick, msg)


def reply(nick, msg, chan=None):
    if chan:
        say(chan, nick + ': ' + msg)
    else:
        say(nick, msg)


def kick(nick, chan, why=''):
    send_msg('KICK', chan, nick, why)


def mode(chan, flag, arg):
    send('MODE', chan, flag, arg)


def time_ban(time, nick, chan, why='', prefix=None):
    prefix = prefix or nick + '!*@*'
    mode(chan, '+b', prefix)

    kick(nick, chan, why)

    if time > -1:
        Timer(time, lambda: mode(chan, '-b', prefix)).start()
