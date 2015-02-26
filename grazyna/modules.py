from . import config, format, irc, plugins
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
re_cmd = re.compile('^(?:%s: |\.)(\S+)(?: (.*)|)$' % config.nick)


class ModuleManager(object):

    config = None
    plugins = None

    def __init__(self, config):
        self.config = config
        self.plugins = []


    def load_all(self):
        plugins = self.config['plugins']
        for name, module_path in plugins.items():
            self.load(name, module_path)

    def load(self, name, module_path):
        module = __import__(module_path)
        reload(module)
        self.plugins[name] = [
            obj for obj in module.__dict__.values()
            if getattr(obj, 'is_bot_event', False) is True
        ]

    def remove(self, name):
        module = self.plugins[name]
        del self.plugins[name]


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

        if not((private and event.on_private)
               or (not private and event.on_channel)):
            continue

        if event.is_reg:
            match = event.compiled_reg.search(msg)
            if match:
                args = match.groups()
                kwargs = match.groupdict()
            else:
                continue
        else:
            if cmd != event.cmd:
                continue

            if text:
                args, kwargs = get_args_from_text(text, event.max_args)

        bot = RequestBot(
            protocol=protocol,
            private=private,
            chan=channel,
            user=user
        )

        if event.admin_required and not bot.is_admin():
            break

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

        try:
            dict_arg = check_type(args, kwargs, event)
        except Exception as e:
            break

        try:
            event(bot, **dict_arg)
        except:
            traceback.print_exc(file=sys.stdout)
            tb = traceback.format_exc().split('\n')[-4:-1]
            protocol.reply(
                user.nick,
                format.bold('ERR: ') + tb[2] +
                format.color(tb[0], format.color.red),
                channel
            )
        if not event.next:
            break
