#!/usr/bin/python3
"""
Hasla i takie tam
"""
import grazyna.auths
from grazyna.plugins.czy import czy as czy_plugin

host = 'irc.quakenet.org'
admin = ('firemark',)

plugins = {
    'admin': 'grazyna.plugins.admin',
    'czy': czy_plugin(cmd='czy', answers="conf_files/czy.txt")
}
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
log_dir = "log"
# channels = ('#testtest',)
