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
    first_name = user.first_name or "—"
    mention = user.mention
    username = f"@{user.username}" if user.username else "—"

    # Get user bio
    try:
        full_info = await bot.get_chat(user_id)
        bio = full_info.bio or "—"
    except:
        bio = "—"

    chakra = await get_user_chakra(user_id)

    # Determine title
    try:
        member = await bot.get_chat_member(message.chat.id, user_id)
        if member.status == "creator":
            role = "👑 Owner"
        elif member.status == "administrator":
            role = "⚔️ Admin"
        else:
            role = "👤 Member"
    except:
        role = "❓ Unknown"

    # Premium status — placeholder for now
    premium = "False"

    # Naruto Style Caption
    caption = f"""
─────⌈✦ 𝗨𝘀𝗲𝗿 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 ✦⌋──────

✦ 𝗨𝘀𝗲𝗿 𝗜𝗗: `{user_id}`
✦ 𝗙𝗶𝗿𝘀𝘁 𝗡𝗮𝗺𝗲: {first_name}
✦ 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {username}
✦ 𝗟𝗶𝗻𝗸: {mention}
✦ 𝗕𝗶𝗼: {bio}

✦ 𝗚𝗹𝗼𝗯𝗮𝗹 𝗖𝗵𝗮𝗸𝗿𝗮 𝗣𝗼𝗶𝗻𝘁𝘀: `{chakra}` 🍥

✦ 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗨𝘀𝗲𝗿? {premium}
✦ 𝗣𝗿𝗲𝘀𝗲𝗻𝗰𝗲: {role}

╭────────────────────╮  
│   𝑵𝒂𝒓𝒖𝒕𝒐 𝑺𝒕𝒚𝒍𝒆   │  
╰────────────────────╯
"""

    # Try sending profile photo
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
