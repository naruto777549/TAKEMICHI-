import random
import string
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from revengers import bot
from revengers.db import file_collection, Banned

BOT_USERNAME = "UzumakiFileHavenbot"

# ─── only UPDATE channel ────────────────────────────────────────────────────────
CHANNELS = [
    ("Bey_war_updates", "ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ")   # public username (bot must be admin/member)
]

# ─── force‑sub check (now for a single channel) ────────────────────────────────
async def check_subscription(bot, message: Message) -> bool:
    user_id = message.from_user.id
    for channel, name in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status in ("left", "kicked"):
                raise UserNotParticipant
        except Exception:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton(name, url=f"https://t.me/{channel}")]
            ])
            await message.reply(
                f"›› ʜᴇʏ {message.from_user.mention} ×\n\n"
                "```#JOIN CHANNEL\nʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ,\n"
                "sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs.```",
                reply_markup=buttons
            )
            return False
    return True


def generate_code(length: int = 5) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@bot.on_message(filters.command("genlink") & filters.private)
async def genlink_handler(bot, message: Message):
    # block banned users
    if message.from_user.id in Banned:
        return await message.reply("🚫 You are banned from using this bot.")

    # force‑sub (only update channel)
    if not await check_subscription(bot, message):
        return

    # must reply to a media
    if not message.reply_to_message or not (
        message.reply_to_message.video or message.reply_to_message.photo
    ):
        return await message.reply(
            "❗ Reply to a video or image to generate a link.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(CHANNELS[0][1], url=f"https://t.me/{CHANNELS[0][0]}")]]
            )
        )

    # generate unique code + save
    code  = generate_code()
    link  = f"https://t.me/{BOT_USERNAME}?start={code}"
    media = message.reply_to_message.video or message.reply_to_message.photo

    await file_collection.insert_one({
        "code"   : code,
        "file_id": media.file_id,
        "caption": message.reply_to_message.caption,
        "type"   : "video" if message.reply_to_message.video else "photo"
    })

    # done
    await message.reply(
        f"📎 Here's your file link:\n<code>{link}</code>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(CHANNELS[0][1], url=f"https://t.me/{CHANNELS[0][0]}")]]
        )
    )