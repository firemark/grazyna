'''
Threads to receive messages and execute plugins
'''
from threading import Thread
from . import waiting_events
from .. import irc, log, config, threads
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
            pass


def execute_func():
    while True:
        event_type, user, args = waiting_events.get()
        if event_type == "msg":
            execute_msg_event(args["chan"], user, args["txt"])


def ping_func():
    while True:
        receive.join(90)
        irc.send('PING', 'Grazyna')
        threads.ping_counter += 1
        if threads.ping_counter > 3 or True:
            irc.send_msg('QUIT', 'Ping Timeout')
            irc.restart()
            irc.connect()

            sleep(1)

            receive.start()

receive = Thread(target=receive_func)
execute = Thread(target=execute_func)
ping = Thread(target=ping_func)
