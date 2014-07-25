#!/usr/bin/python3
from . import config

files = {};

def write(channel, msg):
    if channel not in files:
        files[channel] = open(config.log_dir + '/' + channel,"at")
    files[channel].write( msg )    
    files[channel].flush()
