from grazyna.models import Message
from grazyna.utils import register


@register(cmd='add', on_private=False)
def add_cmd(bot, key, message):
    if not bot.protocol.db:
        return
    with bot.protocol.get_session() as session:
        session.add(Message(
            key=key,
            channel=bot.chan,
            message=message,
        ))
    bot.reply('Done!')


@register(cmd='del', on_private=False, admin_required=True)
def delete_cmd(bot, key):
    if not bot.protocol.db:
        return
    with bot.protocol.get_session() as session:
        session.query(Message).filter_by(key=key, channel=bot.chan).delete()
    bot.reply('Done!')

