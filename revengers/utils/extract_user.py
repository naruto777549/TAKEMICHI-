from pyrogram.types import Message
from revengers import bot

async def extract_user_id(message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        return user.id, user.first_name

    if len(message.command) < 2:
        return None, None

    arg = message.command[1]

    if arg.startswith("@"):
        try:
            user = await bot.get_users(arg)
            return user.id, user.first_name
        except:
            return None, None

    if arg.isdigit():
        return int(arg), None

    return None, None