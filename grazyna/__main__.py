#!/usr/bin/python3
from sys import argv
from . import config
from .irc import client


def load_config(filename):
    pass


def run():
    cfg = load_config(argv[1])
    client.connect(cfg)


if __name__ == "__main__":
    run()
