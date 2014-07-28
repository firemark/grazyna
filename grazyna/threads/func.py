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

            if command == '005' and not irc.ready:
                irc.ready = True
                ping.start()
                for channel in config.channels:
                    irc.send('JOIN', channel)

                try:
                    # irc.say('Q@CServe.quakenet.org',
                    #        'AUTH %s %s' % (config.auth['user'],
                    #                        config.auth['pass'])
                    #        )
                    irc.say('nickserv', 'identify %s' % config.auth['pass'])
                except:
                    pass
            elif prefix == 'PING':
                #print ('*PONG*')
                irc.send('PONG', data[1])


            elif command == '330':  # I don't have idea where is in RFC
                nick, account = data[3:5]

                if (is_admin_con.nick == nick
                   and account in config.admin):
                    is_admin_con.nick = None
                    is_admin_con.set()
            elif command in ('PRIVMSG', 'NOTICE'):
                #modules.use(chan, nick, text)


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
