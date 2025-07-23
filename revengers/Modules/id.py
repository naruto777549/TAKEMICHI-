from pyrogram import filters
from pyrogram.types import Message
from ProFileRenamer import bot 

@bot.on_message(filters.command("id"))
async def get_ids(bot, message: Message):
    msg_id = message.id
    user_id = message.from_user.id
    chat_id = message.chat.id

    text = f"""
<b>ᴍᴇssᴀɢᴇ ɪᴅ:</b> <code>{msg_id}</code>
<b>ʏᴏᴜʀ ɪᴅ:</b> <code>{user_id}</code>
<b>ᴄʜᴀᴛ ɪᴅ:</b> <code>{chat_id}</code>
"""

    await message.reply(text)