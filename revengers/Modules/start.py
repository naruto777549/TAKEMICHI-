from pyrogram import filters
from pyrogram.types import Message
from revengers import bot


@bot.on_message(filters.command("start") & filters.private)
async def start_command(_, message: Message):
    await message.reply_text(
        "👋 Hello!\n\n"
        "I am alive and ready to work 🚀"
    )