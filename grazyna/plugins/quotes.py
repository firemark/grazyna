import random
from ..utils import register, create_help

#create_help('czy', '?czy <pytanie>')


@register(cmd='{cmd}')
def quotes(bot, ask=None):
    replies = get_replies(bot)
    reply = random.choice(replies)
    bot.reply(reply)


def get_replies(bot):
    """funny random quotes"""
    replies = bot.plugin.temp.get('replies')
    if replies is None:
        pathname = bot.config['file']
        with open(pathname) as f:
            replies = f.read().splitlines()
        bot.plugin.temp['replies'] = replies
    return replies
