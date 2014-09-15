#!/usr/bin/python3
from . import config
from datetime import datetime


files = {};

def write(channel, msg):
    str_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    if channel not in files:
        files[channel] = open(config.log_dir + '/' + channel, "at")
    file_log = files[channel]
    file_log.write('[%s] %s\r\n"' % (str_datetime, msg))  
    file_log.flush()
