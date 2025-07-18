import random
import string
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from revengers import bot
from revengers.db import file_collection, Banned

BOT_USERNAME = "UzumakiFileHavenbot"

# Use channel username or ID
CHANNELS = [
    ("Bey_war_updates", "ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ"),            # Public username (no @ or link)
    ("-1002523949507", "sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ")               # Private channel ID (bot must be a member)
]

async def check_subscription(bot, message: Message):
    user_id = message.from_user.id
    for channel, name in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status in ("left", "kicked"):
                raise UserNotParticipant
        except:
            # Buttons to all channels
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton(name, url=f"https://t.me/{channel.replace('-100', 'c/')}")] if channel.startswith("-100")
                else [InlineKeyboardButton(name, url=f"https://t.me/{channel}")]
                for channel, name in CHANNELS
            ])
            await message.reply(
                f"›› ʜᴇʏ {message.from_user.mention} ×\n\n"
                "```#JOIN CHANNEL\nʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ,\n"
                "sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs.```",
                reply_markup=buttons
            )
            return False
    return True


def generate_code(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@bot.on_message(filters.command("genlink") & filters.private)
async def genlink_handler(bot, message: Message):
    if message.from_user.id in Banned:
        return await message.reply("🚫 You are banned from using this bot.")

    if not await check_subscription(bot, message):
        return

    if not message.reply_to_message or not (
        message.reply_to_message.video or message.reply_to_message.photo
    ):
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(CHANNELS[0][1], url=f"https://t.me/{CHANNELS[0][0]}")]]
        )
        return await message.reply(
            "❗ Reply to a video or image to generate a link.",
            reply_markup=buttons
        )

    code = generate_code()
    link = f"https://t.me/{BOT_USERNAME}?start={code}"
    media = message.reply_to_message.video or message.reply_to_message.photo
    file_id = media.file_id
    caption = message.reply_to_message.caption

    await file_collection.insert_one({
        "code": code,
        "file_id": file_id,
        "caption": caption,
        "type": "video" if message.reply_to_message.video else "photo"
    })

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton(CHANNELS[0][1], url=f"https://t.me/{CHANNELS[0][0]}")]]
    )

    await message.reply(
        f"📎 Here's your file link:\n<code>{link}</code>",
        reply_markup=buttons
    )