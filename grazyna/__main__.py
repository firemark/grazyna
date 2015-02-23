#!/usr/bin/python3
from importlib.machinery import SourceFileLoader
from sys import argv


def run():
    from . import config
    conf = SourceFileLoader("config", argv[1]).load_module()

    for var in dir(conf): # I know, hack
        setattr(config, var, getattr(conf, var))

    from .irc import client
    from . import modules
    modules.load()
    client.connect()


if __name__ == "__main__":
    run()
