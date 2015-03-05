from . import format
from .request import RequestBot
import re
from importlib import reload
import traceback
import sys
import time
from collections import defaultdict
from inspect import getcallargs

users = {}
lasttime = 0
modules = defaultdict(list)
event_types = ("msg", "kick")

# set defaultdicts in events
events = {
    event_type: {}
    for event_type in event_types
}

re_split = re.compile(r' *(?:(\w+)[:=] *)?(?:"([^"]+)"|(\S+))')
#re_cmd = re.compile('^(?:%s: |\.)(\S+)(?: (.*)|)$' % config.nick)


class ModuleManager(object):

    protocol = None
    plugins = None

    def __init__(self, protocol):
        self.protocol = protocol
        self.plugins = {}

    @property
    def config(self):
        return self.protocol.config

    def load_all(self):
        for name, module_path in self.config.items('plugins'):
            self.load(name, module_path)

    def load(self, name, module_path):
        print(name, module_path)
        path, module_name = module_path.rsplit(".", 1)
        module = __import__(module_path, globals(), locals(), [module_name])
        reload(module)
        self.plugins[name] = [
            obj for obj in module.__dict__.values()
            if getattr(obj, 'is_bot_event', False) is True
        ]

    def remove(self, name):
        module = self.plugins[name]
        del self.plugins[name]

    def execute(self, channel, user, msg):
        cmd, text = self.get_cmd_and_text(msg)
        private = channel[0] != "#"

        if cmd is not None:
            self.execute_command(cmd, text, private, channel, user)

        self.execute_regs(msg, private, channel, user)

    def execute_command(self, cmd, text, private, channel, user):
        name, func = self.find_command(cmd, private)
        if func is None:
            return

        if text:
            args, kwargs = get_args_from_text(text, func.max_args)
        else:
            args = []
            kwargs = {}

        self.execute_func(func, name, private, channel, user, args, kwargs)

    def execute_regs(self, msg, private, channel, user):
        for name, func, matches in self.find_regs(msg, private):
            for match in matches:
                args = match.groups()
                kwargs = match.groupdict()
                self.execute_func(func, name, private, channel, user,
                                  args, kwargs)

    def find_function_in_plugin_with_name(self, predicate, private):
        return (
            (name, func)
            for name, plugin in self.plugins.items()
            for func in plugin
            if (
                (
                    (not private and func.on_channel)
                    or (private and func.on_private)
                )
                and predicate(func, name)
            )
        )

    def find_command(self, cmd, private):
        return next(
            self.find_function_in_plugin_with_name(
                lambda func, name: (
                    func.is_reg is False
                    and func.cmd.format(self.get_plugin_cfg(name)) == cmd
                ),
                private
            ),
            None
        )

    def find_regs(self, msg, private):
        return (
            (name, func, func.compiled_reg.finditer(msg))
            for name, func in self.find_function_in_plugin_with_name(
                lambda func, name: func.is_reg is True,
                private
            )
        )

    def get_plugin_cfg(self, name):
        cfg = self.config
        plugin_name = 'plugin:%s' % name
        if cfg.has_section(plugin_name):
            return cfg.items(plugin_name)
        else:
            return {}

    def get_cmd_and_text(self, msg):
        cfg = self.config['main']
        startswith = lambda key: msg.startswith(cfg[key])
        if startswith('command-prefix'):
            data = msg.split(maxsplit=1)
            cmd = data[0][1:]
        elif startswith('nick'):
            data = msg.split(maxsplit=2)[1:]
            cmd = data[0]
        else:
            return None, msg
        text = data[1] if len(data) > 1 else ""
        return cmd, text

    def execute_func(self, func, name, private, channel, user, args, kwargs):
        bot = RequestBot(
            protocol=self.protocol,
            private=private,
            chan=channel if not private else None,
            config=self.get_plugin_cfg(name),
            user=user
        )

        try:
            dict_arg = check_type(args, kwargs, func)
        except:
            pass

        if func.admin_required and not bot.is_admin():
            return

        try:
            func(bot, **dict_arg)
        except:
            traceback.print_exc(file=sys.stdout)
            tb = traceback.format_exc().split('\n')[-4:-1]
            self.protocol.reply(
                user.nick,
                format.bold('ERR: ') + tb[2] +
                format.color(tb[0], format.color.red),
                channel
            )


def get_args_from_text(text, max_args):
    args = []
    kwargs = {}
    for arg_group in re_split.finditer(text):
        arg_name, arg_quotes, arg = arg_group.groups()
        arg = arg_quotes or arg

        if arg_name:
            kwargs[arg_name] = arg
        else:
            if max_args > -1:
                args.append(arg)

    if len(args) > max_args != -1:
        last_arg = ' '.join(args[max_args:])
        args = args[0:max_args]
        try:
            args[-1] += ' ' + last_arg
        except IndexError:
            args = [last_arg]

    return args, kwargs


def check_type(args, kwargs, event):
    dict_arg = getcallargs(event, None, *args, **kwargs)
    for key, item in dict_arg.items():
        arg_type = event.__annotations__.get(key, str)
        if item != None:
            dict_arg[key] = arg_type(item)
    del dict_arg['bot']
    return dict_arg



#OLD - ignore this
def execute_msg_event(protocol, channel, user, msg):
    global lasttime
    nick = user.nick
    #print(channel, user, msg)

    # match if is a command
    cmd_match = re_cmd.match(msg)
    if cmd_match:
        cmd, text = cmd_match.groups()
    else:
        cmd = None

    if channel[0] != "#":
        channel = None
        private = True
    else:
        private = False

    for event in events["msg"].values():
        args = []
        kwargs = {}

        if event.block:
            # filtr antyspamowy, nienawidze was
            newtime = time.time()
            #print(lasttime, newtime)
            if lasttime < newtime:
                lasttime = newtime + config.tasks[1]
                users.clear()
            if nick not in users:
                users[nick] = 1
            else:
                if users[nick] < config.tasks[0]:
                    users[nick] += 1
                else:
                    break


        if not event.next:
            break
