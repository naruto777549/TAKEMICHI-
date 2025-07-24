from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db.chakra_db import get_top_chakra

@bot.on_message(filters.command("topchakra") & filters.group)
async def top_chakra(bot, message: Message):
    text = "**🏆 Top Chakra Holders:**\n\n"
    async for user in get_top_chakra():
        user_id = user["_id"]
        points = user["chakra"]
        try:
            user_info = await bot.get_users(user_id)
            text += f"• [{user_info.first_name}](tg://user?id={user_id}) — `{points}` Chakra\n"
        except:
            text += f"• Unknown (`{user_id}`) — `{points}` Chakra\n"

    await message.reply(text)