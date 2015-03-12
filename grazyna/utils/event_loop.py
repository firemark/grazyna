import asyncio
import sys
import traceback
from random import random

def loop(time_config_key, default):
    def outter(func):
        @asyncio.coroutine
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
                        func(protocol, plugin, cfg)
                    except:
                        traceback.print_exc(file=sys.stdout)


                yield from asyncio.sleep(time_to_sleep)
        inner.is_loop = True
        return inner
    return outter


