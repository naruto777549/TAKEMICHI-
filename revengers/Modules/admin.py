from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Admins
from revengers.helpers.is_admin import is_admin

@bot.on_message(filters.command("add_admin") & (filters.group | filters.private) & is_admin)
async def add_admin(bot, message: Message):
    user_id, name = await extract_user_id(message)

    if not user_id:
        return await message.reply("❗ Usage: `/add_admin @username`, `/add_admin user_id`, or reply to the user.", quote=True)

    existing = await Admins.find_one({"_id": user_id})
    if existing and existing.get("is_admin", False):
        return await message.reply(f"⚠️ `{user_id}` is already an admin.")

    await Admins.update_one({"_id": user_id}, {"$set": {"is_admin": True}}, upsert=True)
    return await message.reply(f"✅ User `{user_id}` has been added as admin.", quote=True)