from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Admins
from revengers.utils.checks import is_admin


@bot.on_message(filters.command("list_admin") & filters.private)
async def list_admins_cmd(bot, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You're not authorized to use this command.")

    cursor = Admins.find()
    admin_list = []
    async for admin in cursor:
        admin_id = admin["_id"]
        try:
            user = await bot.get_users(admin_id)
            admin_list.append(f"• {user.mention} (`{admin_id}`)")
        except:
            admin_list.append(f"• `{admin_id}`")

    if not admin_list:
        return await message.reply("⚠️ No admins found.")

    text = "**👑 Current Admins:**\n\n" + "\n".join(admin_list)
    await message.reply(text)