from grazyna.utils import register


@register(cmd='utf8')
def utf(bot):
    """show utf-8 chars"""
    bot.reply("żółw,lwiątko,kurczę")
