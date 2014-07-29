'''
Threads to receive messages and execute plugins
'''
from threading import Thread
from . import is_admin_con, waiting_events
from .. import irc, log, config
from ..irc import User
from ..modules import execute_msg_event
from datetime import datetime as dt
from time import sleep, time
import sys


def receive_func():
    print("RUN!")

    saved_time = dt.now()

    while True:
        for data in irc.recv():
            #print(data, (dt.now() - saved_time).total_seconds())
            saved_time = dt.now()
            prefix, command = data[0:2]
            user = User(prefix)

            # elif data[1] == 'QUIT':
            #    log.write(data[2] , "[%s] %s::QUIT"  % ( time.strftime("%d-%m-%Y %H:%M:%S") , data[0].split('!')[0][1:] ) )

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
