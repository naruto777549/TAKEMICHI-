from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import get_user_chakra
from pyrogram.errors import PeerIdInvalid

@bot.on_message(filters.command("info") & filters.group)
async def user_info(bot, message: Message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    user_id = user.id
    mention = user.mention
    username = f"@{user.username}" if user.username else "No Username"

    # Get user bio
    try:
        full_info = await bot.get_chat(user_id)
        bio = full_info.bio or "No Bio"
    except:
        bio = "No Bio"

    # Get Chakra points from database
    user_data = await get_user_chakra(user_id)
    points = user_data.get("chakra", 0) if user_data else 0

    # Check if admin
    try:
        member = await bot.get_chat_member(message.chat.id, user_id)
        status = member.status
        if status == "creator":
            title = "Owner 👑"
        elif status == "administrator":
            title = "Admin 🔱"
        else:
            title = "Member"
    except:
        title = "Unknown"

    # Caption
    caption = f"""
✦✧✦✦✧✦✦✧✦✦✧✦✦✧✦✦✧✦✦✧✦
✧        🌌  {mention}  🌌        ✧
✦✧✦✦✧✦✦✧✦✦✧✦✦✧✦✦✧✦✦✧✦
║ Username: {username}
║ User ID: `{user_id}`
║ Title: {title}
║ Chakra: `{points}`
║ Bio: {bio}
✧✦✧✦✦✧✦✦✧✦✦✧✦✦✧✦✦✧✦✦✧
✦        🌙  NARUTO STYLE  🌙        ✦
✧✦✧✦✦✧✦✦✧✦✦✧✦✦✧✦✦✧✦✦✧
"""

    # Send profile photo with caption
    try:
        photos = await bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            await message.reply_photo(photos.photos[0].file_id, caption=caption)
        else:
            await message.reply(caption)
    except PeerIdInvalid:
        await message.reply("Can't fetch profile photo.")