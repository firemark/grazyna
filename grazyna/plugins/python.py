from grazyna.utils import register


@register(cmd='pep')
def pep(bot, number: int):
    """show pep X link"""
    msg = 'https://www.python.org/dev/peps/pep-{:04}/'.format(number)
    bot.reply(msg)
