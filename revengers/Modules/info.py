from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid
from pyrogram.raw.functions.photos import GetUserPhotos

from revengers import bot
from revengers.db import get_user_chakra

@bot.on_message(filters.command("info") & filters.group)
async def user_info(bot, message: Message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    user_id = user.id
    mention = user.mention
    username = f"@{user.username}" if user.username else "—"

    # Get user bio
    try:
        full_info = await bot.get_chat(user_id)
        bio = full_info.bio or "—"
    except:
        bio = "—"

    # Chakra points
    chakra = await get_user_chakra(user_id)

    # Determine role/title
    try:
        member = await bot.get_chat_member(message.chat.id, user_id)
        if member.status == "creator":
            title = "👑 Owner"
        elif member.status == "administrator":
            title = "🛡️ Co-Owner" if member.can_manage_chat else "⚔️ Admin"
        else:
            title = "👤 Member"
    except:
        title = "❓ Unknown"

    # Naruto style caption
    caption = f"""
🍥 𝗨𝘇𝘂𝗺𝗮𝗸𝗶 𝗖𝗵𝗮𝗸𝗿𝗮 𝗦𝗲𝗻𝘀𝗲 🍥

👤 Name: {mention}
🔗 Username: {username}
🆔 ID: `{user_id}`
🎖️ Title: {title}
💠 Chakra: `{chakra}`
📝 Bio: {bio}

━━━━━━━━━━━━━━━━━━
🌀 Powered by NARUTO BOT 🌀
"""

    # Try getting profile photo using raw API
    try:
        user_peer = await bot.resolve_peer(user_id)
        photos = await bot.invoke(GetUserPhotos(
            user_id=user_peer,
            offset=0,
            max_id=0,
            limit=1
        ))

        if photos.photos:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photos.photos[0],
                caption=caption,
                reply_to_message_id=message.id
            )
        else:
            await message.reply(caption)
    except PeerIdInvalid:
        await message.reply("Unable to fetch profile photo.")
    except Exception as e:
        print(f"Error fetching profile photo: {e}")
        await message.reply(caption)