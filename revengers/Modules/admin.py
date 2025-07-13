# Modules/admin.py

from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Admins

OWNER_ID = 7576729648  # Replace with your actual owner ID


async def extract_user_id(message: Message):
    # 1. If user replied to someone
    if message.reply_to_message:
        return message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name

    # 2. If argument is missing
    if len(message.command) < 2:
        return None, None

    arg = message.command[1]

    # 3. If username
    if arg.startswith("@"):
        try:
            user = await bot.get_users(arg)
            return user.id, user.first_name
        except:
            return None, None

    # 4. If numeric ID
    if arg.isdigit():
        return int(arg), None

    return None, None


@bot.on_message(filters.command("add_admin") & filters.user(OWNER_ID))
async def add_admin(bot, message: Message):
    user_id, name = await extract_user_id(message)

    if not user_id:
        return await message.reply("❗ Usage: `/add_admin @username`, `/add_admin user_id`, or reply to the user.", quote=True)

    await Admins.update_one({"_id": user_id}, {"$set": {"is_admin": True}}, upsert=True)
    return await message.reply(f"✅ User `{user_id}` has been added as admin.", quote=True)