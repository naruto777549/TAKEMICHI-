from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from revengers import bot

@bot.on_message(filters.command("help") & filters.private)
async def help_command(bot, message: Message):
    user_mention = message.from_user.mention
    image_url = "https://files.catbox.moe/wggk0a.jpg"

    caption = f"""
⁉️ Hᴇʏ...!! {user_mention} ~

```➪ I ᴀᴍ ᴀ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇ sʜᴀʀɪɴɢ ʙᴏᴛ, ᴍᴇᴀɴᴛ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ғɪʟᴇs ᴀɴᴅ ɴᴇᴄᴇssᴀʀʏ sᴛᴜғғ ᴛʜʀᴏᴜɢʜ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ ғᴏʀ sᴘᴇᴄɪғɪᴄ ᴄʜᴀɴɴᴇʟs.

➪ Iɴ ᴏʀᴅᴇʀ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇs ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ᴀʟʟ ᴍᴇɴᴛɪᴏɴᴇᴅ ᴄʜᴀɴɴᴇʟ ᴛʜᴀᴛ ɪ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴛᴏ ᴊᴏɪɴ. Yᴏᴜ ᴄᴀɴ ɴᴏᴛ ᴀᴄᴄᴇss ᴏʀ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇs ᴜɴʟᴇss ʏᴏᴜ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟs.

➪ Sᴏ ᴊᴏɪɴ Mᴇɴᴛɪᴏɴᴇᴅ Cʜᴀɴɴᴇʟs ᴛᴏ ɢᴇᴛ Fɪʟᴇs ᴏʀ ɪɴɪᴛɪᴀᴛᴇ ᴍᴇssᴀɢᴇs...```

‣ /help - Oᴘᴇɴ ᴛʜɪs ʜᴇʟᴘ ᴍᴇssᴀɢᴇ !
◈ Sᴛɪʟʟ ʜᴀᴠᴇ ᴅᴏᴜʙᴛs, ᴄᴏɴᴛᴀᴄᴛ ʙᴇʟᴏᴡ ᴘᴇʀsᴏɴs/ɢʀᴏᴜᴘ ᴀs ᴘᴇʀ ʏᴏᴜʀ ɴᴇᴇᴅ !
"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ ɢʀᴏᴜᴘ", url="https://t.me/+ZyRZJntl2FU0NTk1")
        ],
        [
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/Uzumaki_X_Naruto_6"),
            InlineKeyboardButton("ᴅᴇᴠʟᴏᴘᴇʀ", url="https://t.me/Uzumaki_X_Naruto_6")
        ]
    ])

    await message.reply_photo(
        photo=image_url,
        caption=caption,
        reply_markup=buttons
    )