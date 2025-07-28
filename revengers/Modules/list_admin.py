from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode, ChatType
from revengers import bot
from revengers.db import Admins
from revengers.utils.checks import is_admin

@bot.on_message(filters.command("list_admin"))
async def list_admins_cmd(bot, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You're not authorized to use this command.")

    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.reply_text("ℹ️ Please use this command in private chat (DM) only.")

    admin_list = []
    async for admin in Admins.find():
        admin_id = admin["_id"]
        try:
            user = await bot.get_users(admin_id)
            admin_list.append(f"║ 🔹 [{user.first_name}](tg://user?id={admin_id}) (`{admin_id}`)")
        except:
            admin_list.append(f"║ 🔹 Unknown User (`{admin_id}`)")

    if not admin_list:
        return await message.reply("⚠️ No admins found.")

    text = (
        "★════════════════════➽\n"
        "║ 👑 𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟 👑\n"
        "★════════════════════➽\n"
        "║\n"
        "║ 🔹 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗔𝗱𝗺𝗶𝗻𝘀:\n"
        + "\n".join(admin_list) + "\n"
        "║\n"
        f"║ 🔹 𝗧𝗼𝘁𝗮𝗹 :- {len(admin_list)} Admin(s)\n"
        "★════════════════════➽"
    )

    await message.reply(
        text,
        parse_mode=ParseMode.MARKDOWN
    )