# handlers/admin.py
from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Admins

OWNER_ID = 7576729648  

@bot.on_message(filters.command("add_admin") & filters.user(OWNER_ID))
async def add_admin(bot, message: Message):
    if len(message.command) != 2:
        return await message.reply("❗ Usage: `/add_admin user_id`", quote=True)

    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("❗ Invalid ID format.", quote=True)

    await Admins.update_one({"_id": user_id}, {"$set": {"is_admin": True}}, upsert=True)
    await message.reply(f"✅ User `{user_id}` has been added as admin.", quote=True)