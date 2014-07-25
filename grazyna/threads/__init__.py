from threading import Thread, Event
from queue import Queue
from ..irc import send


waiting_events = Queue()
is_admin_con = Event()
is_admin_con.nick = None


def is_admin(nick):
    is_admin_con.nick = nick
    is_admin_con.clear()
    send('WHOIS', nick)
    return is_admin_con.wait(2)
