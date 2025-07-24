from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.utils.is_admin import is_admin
from revengers.utils.extract_user import extract_user_id
from revengers.db import add_admin, is_admin as check_admin

@bot.on_message(filters.command("add_admin") & (filters.group | filters.private) & is_admin)
async def add_admin_cmd(bot, message: Message):
    user_id, name = await extract_user_id(message)

    if not user_id:
        return await message.reply(
            "❗ Usage: `/add_admin @username`, `/add_admin user_id`, or reply to a user.",
            quote=True
        )

    if await check_admin(user_id):
        return await message.reply(f"⚠️ `{user_id}` is already an admin.")

    await add_admin(user_id)
    return await message.reply(f"✅ `{name or user_id}` has been added as admin.", quote=True)