from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Banned
from config import ADMINS


async def extract_user_id(message: Message) -> int | None:
    # 1. From reply
    if message.reply_to_message:
        return message.reply_to_message.from_user.id

    # 2. From command args
    if len(message.command) < 2:
        return None

    arg = message.command[1]

    # Username format
    if arg.startswith("@"):
        try:
            user = await bot.get_users(arg)
            return user.id if user else None
        except:
            return None

    # Numeric ID format
    if arg.isdigit():
        return int(arg)

    return None


@bot.on_message(filters.command("ban") & filters.private)
async def ban_user(bot, message: Message):
    if message.from_user.id not in ADMINS:
        return

    user_id = await extract_user_id(message)

    if not user_id:
        return await message.reply("❌ Usage: `/ban @username`, `/ban user_id`, or reply to a user's message.", quote=True)

    if user_id in Banned:
        return await message.reply("⚠️ User is already banned.", quote=True)

    Banned.append(user_id)
    await message.reply(f"✅ User `{user_id}` has been banned.", quote=True)


@bot.on_message(filters.command("unban") & filters.private)
async def unban_user(bot, message: Message):
    if message.from_user.id not in ADMINS:
        return

    user_id = await extract_user_id(message)

    if not user_id:
        return await message.reply("❌ Usage: `/unban @username`, `/unban user_id`, or reply to a user's message.", quote=True)

    if user_id not in Banned:
        return await message.reply("⚠️ User is not banned.", quote=True)

    Banned.remove(user_id)
    await message.reply(f"✅ User `{user_id}` has been unbanned.", quote=True)