'''
Useful decorators and function
'''
import asyncio
import re
import inspect


def create_help(cmd, txt):
    pass


def init_plugin(func):
    func.is_initial = True
    return func


class register(object):
    default_kwargs = {
        "on_private": True,
        "on_channel": True,
        "event": "msg",
        "is_reg": False,
        "reg": None,
        "cmd": None,
        "next": False,
        "name": None,
        "priority": 0,
        "block": True,
        "first_char": '.',
        "admin_required": False,
    }

    def __init__(self, **kwargs):
        """
        :param cmd: Command name. Attributes must have annotations!
        :param reg: regexp without command name.
        :param on_private
        :param on_channel
        :param name alternative name of event. If is not defined then name is function name
        :param next: if is true, accepting another matching commands
        :param priority: 0 is a smallest priority
        :param first_char: char before command name
        :param admin_required: if is true - check permissions
        """

        self.kwargs = self.default_kwargs.copy()

        event_type = kwargs.get("event", "msg")
        reg = kwargs.get("reg", None)
        if reg:
            kwargs['compiled_reg'] = re.compile(reg)
            kwargs["is_reg"] = True
        if event_type == "msg":
            if not(reg or kwargs.get("cmd", None)):
                raise ValueError("Must be 'cmd' or 'reg' argument")
        else:
            raise ValueError("event argument is invalid")

        self.kwargs.update(kwargs)

    def __call__(self, old_func):
        func = asyncio.coroutine(old_func)
        func.__dict__.update(self.kwargs)
        func.is_bot_event = True
        module_name = old_func.__module__.split('.')[-1]

        func.name = '%s.%s' % (module_name, func.name or func.__name__.lower())

        if func.event == "msg":
            argspec = inspect.getfullargspec(old_func)
            if argspec.args:  # count require argument
                len_defaults = len(argspec.defaults) if argspec.defaults else 0
                func.max_args = len(argspec.args) - len_defaults - 1
            else:
                func.max_args = -1

            #events["msg"][func.name] = func
            #modules[module_name].append(func)

        return func
