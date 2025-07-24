from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import get_top_chakra

@bot.on_message(filters.command("rank") & filters.group)
async def top_chakra(bot, message: Message):
    top_users = await get_top_chakra()

    if not top_users:
        return await message.reply("⚠️ No Chakra holders found.")

    text = "🏆 **Top Chakra Holders**\n\n"
    for idx, user in enumerate(top_users, start=1):
        user_id = user["_id"]
        chakra = user.get("chakra", 0)

        try:
            user_info = await bot.get_users(user_id)
            name = user_info.first_name
        except:
            name = "Unknown"

        text += f"🔹 {idx}. [{name}](tg://user?id={user_id}) — `{chakra:,}` Chakra\n"

    await message.reply(text, quote=True)