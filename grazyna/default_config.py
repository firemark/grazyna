#!/usr/bin/python3
"""
Hasla i takie tam
"""


host = 'irc.quakenet.org'
admin = ('firemark',)
plugin = ('ping', 'help', 'ruletka', 'czy', 'admin', 'creeper', 'onp', 'title')
codec = ('utf-8',)
debug = False
ssl = False  # True jezeli wlaczyc ssl
port = 6667
realname = 'GrazynaNg'
ircname = 'Grazynaircbot'
nick = 'Grazyna'
password = 'pass-to-irc'
auth = {'user': 'GrazynaBot', 'pass': 'XX-XX'}
tasks = [
    3,  # ilosc wykonanych zadan na 1 okres na 1 usera
    30  # czas jednego okresu w sekundach
]

bajter_title = {'user': '', 'pass': ''}
channels = ('#test', )
czy_file = "conf_files/czy.txt"
quotes = {
    "latin": "conf_files/latin.txt"
}
log_dir = "log"
# channels = ('#testtest',)
