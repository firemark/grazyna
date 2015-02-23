#!/usr/bin/python3
from sys import argv
from . import config


def run():
    argv[1]
    from .irc import client
    from . import modules
    modules.load()
    client.connect(config)


if __name__ == "__main__":
    run()
