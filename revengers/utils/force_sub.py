# revengers/utils/force_sub.py

from pyrogram.errors import UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

REQUIRED_CHANNELS = [
    ("https://t.me/Bey_war_updates", "Update Channel"),
    ("https://t.me/+ZyRZJntl2FU0NTk1", "Support Group")
]

async def check_force_sub(bot, message: Message):
    user_id = message.from_user.id

    for url, name in REQUIRED_CHANNELS:
        try:
            chat = await bot.get_chat(url.split("/")[-1].replace("+", ""))
            member = await bot.get_chat_member(chat.id, user_id)
            if member.status in ("left", "kicked"):
                raise UserNotParticipant
        except UserNotParticipant:
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton(name, url=url)] for url, name in REQUIRED_CHANNELS]
            )
            return await message.reply(
                f"›› ʜᴇʏ {message.from_user.mention} ×\n\n"
                "``` #JOIN ALL CHANNEL\n"
                "ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, "
                "sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs.```",
                reply_markup=buttons
            )
    return None