#!/usr/bin/python3

import socket, config
import config
from threading import Timer
s = ''
ready = False


def recv():
    global s
    buf = s.recv(5120)
    for codec in config.codec:
        try:
            cmds = buf.decode(codec).split('\r\n')[:-1]
        except:
            continue

        for cmd in (cmd for cmd in cmds if cmd):
            if cmd[0] == ":":
                cmd = cmd[1:]
            cmd = cmd.split(":", 1)
            msg = cmd[0].split()
            if len(cmd) > 1:
                msg.append(cmd[1])
            if len(msg) >= 2:
                yield msg
        break


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


def send(*args):
    global s
    try:
        string = ' '.join((str(arg) for arg in args))[:512] + '\r\n'
        s.send(string.encode())
    except:
        pass


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
