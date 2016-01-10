import asyncio
import sys
import traceback
from functools import wraps
from random import random


def loop(time_config_key, default):
    def outter(old_func):
        func = asyncio.coroutine(old_func)
        @asyncio.coroutine
        @wraps(func)
        def inner(protocol, plugin, future):
            while True:
                if future.cancelled():
                    break
                cfg = protocol.config['plugin:%s' % plugin.name]
                time_to_sleep = cfg.getint(time_config_key, default)
                if time_to_sleep == 0:
                    break

                if protocol.ready:
                    #special random delay
                    yield from asyncio.sleep(random() * 3)
                    try:
                        yield from func(protocol, plugin, cfg)
                    except:
                        traceback.print_exc(file=sys.stdout)


                yield from asyncio.sleep(time_to_sleep)
        inner.is_loop = True
        return inner
    return outter


