from sys import argv
from grazyna.config import create_config
from grazyna.irc import client


def run():
    with open(argv[1]) as f:
        cfg = create_config(f)
    client.connect(cfg)

if __name__ == "__main__":
    run()
