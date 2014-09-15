#!/usr/bin/python3
from imp import load_source
from sys import argv

from .irc import client


def run():
    from . import config
    conf = load_source("config", argv[1])

    for var in dir(conf): # I know, hack
        setattr(config, var, getattr(conf, var))

    #modules.load()
    client.connect()


if __name__ == "__main__":
    run()
