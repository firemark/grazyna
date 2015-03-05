import random
from ..utils import register, create_help

#create_help('czy', '?czy <pytanie>')


@register(cmd='%(cmd)')  # BotArg('alias')
def quotes(bot, ask=None):
    replies = get_replies(bot)
    reply = random.choice(replies)
    bot.reply(reply)


def get_replies(bot):
    plugin_name = bot.config['__name__']
    replies = bot.temp.get('replies')
    if replies is None:
        pathname = bot.config['file']
        with open(pathname) as f:
            replies = f.readlines()
        bot.temp['replies'] = replies
