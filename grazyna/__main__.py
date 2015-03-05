#!/usr/bin/python3
from sys import argv
from .config import create_config
from .irc import client


def load_config(filename):
    pass


def run():
    with open(argv[1]) as f:
        cfg = create_config(f)
    client.connect(cfg)


if __name__ == "__main__":
    run()
