'''
Threads to receive messages and execute plugins
'''
from threading import Thread
from . import waiting_events
from .. import irc, log, config
from ..irc import User
from ..modules import execute_msg_event
from ..message import MessageController
from datetime import datetime as dt
from time import sleep, time
import sys


def receive_func():
    print("RUN!")

    while True:
        for data in irc.recv():
            if data[0] == 'PING':
                irc.send('PONG', data[1])
            else:
                MessageController(data).execute_message()


def execute_func():
    while True:
        event_type, user, args = waiting_events.get()
        if event_type == "msg":
            execute_msg_event(args["chan"], user, args["txt"])


def ping_func():
    while True:
        receive.join(90)
        irc.send('PING', 'Grazyna')


receive = Thread(target=receive_func)
execute = Thread(target=execute_func)
ping = Thread(target=ping_func)
