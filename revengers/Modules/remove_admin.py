from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Admins
from revengers.utils.checks import is_admin

async def extract_user_id(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    if len(message.command) < 2:
        return None
    arg = message.command[1]
    if arg.startswith("@"):
        try:
            user = await bot.get_users(arg)
            return user.id
        except:
            return None
    if arg.isdigit():
        return int(arg)
    return None

@bot.on_message(filters.command("remove_admin") & filters.private)
async def remove_admin_cmd(bot, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You're not authorized to use this.")

    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply("❌ Usage: `/remove_admin @username`, `/remove_admin user_id`, or reply to user.", quote=True)

    if not await is_admin(user_id):
        return await message.reply("⚠️ That user is not an admin.", quote=True)

    await Admins.delete_one({"_id": user_id})
    return await message.reply(f"✅ Removed user `{user_id}` from admin list.", quote=True)