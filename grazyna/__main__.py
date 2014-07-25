#!/usr/bin/python3
from imp import load_source
from sys import argv


def run():
    from . import config
    conf = load_source("config", argv[1])

    for var in dir(conf):
        setattr(config, var, getattr(conf, var))

    # I know, hack

    from . import irc, modules
    from .threads.func import receive, execute, ping

    modules.load()  # loading modules
    irc.connect()  # connect
    receive.start()
    execute.start()
    receive.join()


if __name__ == "__main__":
    run()
