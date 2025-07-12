import random
import string
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from revengers import bot
from revengers.db import file_collection, Banned  # Make sure Banned is imported

BOT_USERNAME = "UzumakiFileHavenbot"
UPDATE_CHANNEL = "https://t.me/Bey_war_updates"

def generate_code(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@bot.on_message(filters.command("genlink") & filters.private)
async def genlink_handler(bot, message: Message):
    # 🚫 Check if the user is banned
    if message.from_user.id in Banned:
        return await message.reply("🚫 You are banned from using this bot.")

    # ✅ Check for reply with video or photo
    if not message.reply_to_message or not (
        message.reply_to_message.video or message.reply_to_message.photo
    ):
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=UPDATE_CHANNEL)]]
        )
        return await message.reply(
            "❗ Reply to a video or image to generate a link.",
            reply_markup=buttons
        )

    # 🔐 Generate unique link
    code = generate_code()
    link = f"https://t.me/{BOT_USERNAME}?start={code}"

    media = message.reply_to_message.video or message.reply_to_message.photo
    file_id = media.file_id
    caption = message.reply_to_message.caption  # original caption (may be None)

    # 💾 Save to DB
    await file_collection.insert_one({
        "code": code,
        "file_id": file_id,
        "caption": caption,
        "type": "video" if message.reply_to_message.video else "photo"
    })

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=UPDATE_CHANNEL)]]
    )

    await message.reply(
        f"📎 Here's your file link:\n<code>{link}</code>",
        reply_markup=buttons
    )