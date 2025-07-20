from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Admins
from revengers.utils.checks import is_admin
from pyrogram.enums import ParseMode, ChatType

@bot.on_message(filters.command("list_admin"))
async def list_admins_cmd(bot, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You're not authorized to use this command.")
    if (message.chat.type==[ChatType.GROUP, ChatType.SUPERGROUP]):
        return await message.reply_text("Use in dm only")
    admin_list = []
    async for admin in Admins.find():
        admin_id = admin["_id"]
        try:
            user = await bot.get_users(admin_id)
            admin_list.append(f"• [{user.first_name}](tg://user?id={admin_id}) (`{admin_id}`)")
        except:
            admin_list.append(f"• Unknown User (`{admin_id}`)")

    if not admin_list:
        return await message.reply("⚠️ No admins found.")

    text = "**👑 Current Admins:**\n\n" + "\n".join(admin_list)
    await message.reply(
        text,
        parse_mode=ParseMode.MARKDOWN
    )
