from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.enums import ChatMemberStatus
from revengers import bot
from datetime import timedelta
import re

# In-memory warn count storage (replace with MongoDB if needed)
user_warns = {}

async def is_admin(chat_id: int, user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]

def extract_user_id(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    parts = message.text.split()
    if len(parts) >= 2:
        if parts[1].startswith("@"):
            return parts[1]
        elif re.match(r"^\d+$", parts[1]):
            return int(parts[1])
    return None

# /ban
@bot.on_message(filters.command("ban") & filters.group)
async def ban_user(bot, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("🚫 Only admins can use this command.")
    
    user_id = extract_user_id(message)
    if not user_id:
        return await message.reply("❌ Please reply to a user or provide @username/user_id.")

    try:
        await bot.ban_chat_member(message.chat.id, user_id)
        await message.reply(f"🔨 Banned successfully.\n👤 ID: `{user_id}`")
    except Exception as e:
        await message.reply(f"❌ Failed to ban: `{e}`")

# /unban
@bot.on_message(filters.command("unban") & filters.group)
async def unban_user(bot, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("🚫 Only admins can use this command.")
    
    user_id = extract_user_id(message)
    if not user_id:
        return await message.reply("❌ Please reply to a user or provide @username/user_id.")

    try:
        await bot.unban_chat_member(message.chat.id, user_id)
        await message.reply(f"✅ Unbanned successfully.\n👤 ID: `{user_id}`")
    except Exception as e:
        await message.reply(f"❌ Failed to unban: `{e}`")

# /mute
@bot.on_message(filters.command("mute") & filters.group)
async def mute_user(bot, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("🚫 Only admins can use this command.")
    
    user_id = extract_user_id(message)
    if not user_id:
        return await message.reply("❌ Please reply to a user or provide @username/user_id.")

    try:
        await bot.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=ChatPermissions(),
        )
        await message.reply(f"🔇 Muted.\n👤 ID: `{user_id}`")
    except Exception as e:
        await message.reply(f"❌ Failed to mute: `{e}`")

# /unmute
@bot.on_message(filters.command("unmute") & filters.group)
async def unmute_user(bot, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("🚫 Only admins can use this command.")
    
    user_id = extract_user_id(message)
    if not user_id:
        return await message.reply("❌ Please reply to a user or provide @username/user_id.")

    try:
        await bot.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            ),
        )
        await message.reply(f"🔈 Unmuted.\n👤 ID: `{user_id}`")
    except Exception as e:
        await message.reply(f"❌ Failed to unmute: `{e}`")

# /warn
@bot.on_message(filters.command("warn") & filters.group)
async def warn_user(bot, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("🚫 Only admins can use this command.")
    
    user_id = extract_user_id(message)
    if not user_id:
        return await message.reply("❌ Please reply to a user or provide @username/user_id.")
    
    key = f"{message.chat.id}:{user_id}"
    user_warns[key] = user_warns.get(key, 0) + 1

    if user_warns[key] >= 3:
        await bot.ban_chat_member(message.chat.id, user_id)
        user_warns[key] = 0
        return await message.reply(f"⚠️ User warned 3 times and has been banned.\n👤 ID: `{user_id}`")
    
    await message.reply(f"⚠️ Warned! ({user_warns[key]}/3)\n👤 ID: `{user_id}`")

# /unwarn
@bot.on_message(filters.command("unwarn") & filters.group)
async def unwarn_user(bot, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("🚫 Only admins can use this command.")

    user_id = extract_user_id(message)
    if not user_id:
        return await message.reply("❌ Please reply to a user or provide @username/user_id.")
    
    key = f"{message.chat.id}:{user_id}"
    user_warns[key] = max(0, user_warns.get(key, 0) - 1)

    await message.reply(f"✅ Warn removed. ({user_warns[key]}/3)\n👤 ID: `{user_id}`")