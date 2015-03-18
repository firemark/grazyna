from ..utils import register
from ..utils.types import regexp

from random import randint


def min_max(num):
    return min(100, max(-100, int(num)))


@register(cmd='roll')
def roll(bot, value:regexp(r'^(\d+)(?:d(-?\d+)(?::(-?\d+))?)?$')):
    """
    usage: .roll 3 || .roll 2d7 || .roll
    """
    many, a, b = value.groups()
    many = int(many)
    if many > 50:
        bot.say('too many steps (%s)!' % many)
        return

    if a is None:
        a, b = 1, 9
    elif b is None:
        a, b = 1, min_max(a)
    else:
        a, b = min_max(a), min_max(b)
        a, b = min(a, b), max(a, b)

    results = [randint(a, b) for i in range(many)]

    bot.reply(
        '({results}) = {sum}'.format(
            results='+'.join(str(x) for x in results),
            sum=sum(results)
        )
    )
