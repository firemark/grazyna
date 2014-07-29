#!/usr/bin/python3
"""
Hasla i takie tam
"""
import grazyna.auths

host = 'irc.quakenet.org'
admin = ('firemark',)
plugin = ('ping', 'help', 'ruletka', 'czy', 'admin', 'creeper', 'onp', 'title')
codec = ('utf-8',)
debug = False
ssl = False
port = 6667
realname = 'GrazynaNg'
ircname = 'Grazynaircbot'
nick = 'Grazyna'
password = 'pass-to-irc'
auth =  grazyna.auths.NonAuth()
# auth = grazyna.auths.QuakenetAuth(user, passwd)
# auth = grazyna.auths.FreenodeAuth(passwd)
tasks = [
    3,  # count executed tasks per user
    30  # one period in seconds
]

bajter_title = {'user': '', 'pass': ''}
channels = ('#test', )
czy_file = "conf_files/czy.txt"
quotes = {
    "latin": "conf_files/latin.txt"
}
log_dir = "log"
# channels = ('#testtest',)
