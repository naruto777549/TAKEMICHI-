import random
import string
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from revengers import bot
from revengers.db import file_collection, Banned

BOT_USERNAME = "UzumakiFileHavenbot"
CHANNELS = [
    ("https://t.me/Bey_war_updates", ""),
    ("https://t.me/+ZyRZJntl2FU0NTk1", "Support Group")
]


async def check_subscription(bot, message: Message):
    user_id = message.from_user.id
    for url, name in CHANNELS:
        try:
            chat = await bot.get_chat(url.split("/")[-1].replace("+", ""))
            member = await bot.get_chat_member(chat.id, user_id)
            if member.status in ("left", "kicked"):
                raise UserNotParticipant
        except:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton(name, url=url)] for url, name in CHANNELS
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
            [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=CHANNELS[0][0])]]
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
        [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=CHANNELS[0][0])]]
    )

    await message.reply(
        f"📎 Here's your file link:\n<code>{link}</code>",
        reply_markup=buttons
    )