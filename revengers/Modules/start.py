from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from revengers import bot
from revengers.db import save_user, save_group

# ✅ Handle /start in private chat
@bot.on_message(filters.command("start") & filters.private)
async def start_private(_, message: Message):
    await save_user(message.from_user.id)
    me = await bot.get_me()

    await message.reply_text(
        """🌀 ᴛᴀɢᴀʟʟ ʙᴏᴛ
➖➖➖➖➖➖➖➖➖➖➖➖
‣ ᴀᴜᴛᴏ-ᴛᴀɢ ᴀʟʟ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs ɪɴ ᴄʜᴜɴᴋs
‣ ᴜsᴇ /tagall ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴇᴠᴇʀʏᴏɴᴇ
‣ sᴜᴘᴘᴏʀᴛs ʀᴇᴘʟʏ + ᴄᴜsᴛᴏᴍ ᴍᴇssᴀɢᴇ
‣ sᴛᴏᴘ ᴛᴀɢ ᴀɴʏᴛɪᴍᴇ ᴜsɪɴɢ /stoptag
➖➖➖➖➖➖➖➖➖➖➖➖
ᴇᴀsʏ ᴛᴏ ᴜsᴇ & ғᴜʟʟʏ ғᴜɴᴄᴛɪᴏɴᴀʟ ᴛᴀɢɢɪɴɢ ʙᴏᴛ ғᴏʀ ɢʀᴏᴜᴘs 🚀""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{me.username}?startgroup=true")],
            [
                InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/Uzumaki_X_Naruto_6"),
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/NARUTO_X_SUPPORT")
            ]
        ]),
        disable_web_page_preview=True
    )


# ✅ Handle /start in groups
@bot.on_message(filters.command("start") & filters.group)
async def start_group(_, message: Message):
    await save_group(message.chat.id)
    await message.reply_text(
        "✅ ʙᴏᴛ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ & sᴀᴠᴇᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.\n\n💡 ᴘʟᴇᴀsᴇ ᴜsᴇ /start ɪɴ ᴅᴍ ғᴏʀ ғᴜʟʟ ᴍᴇɴᴜ"
    ) 