import time
from datetime import timedelta
from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Users, file_collection

start_time = time.time()  # For uptime tracking

def get_readable_time(seconds: int) -> str:
    return str(timedelta(seconds=seconds))

@bot.on_message(filters.command("stats"))
async def stats_handler(bot, message: Message):
    uptime = get_readable_time(int(time.time() - start_time))
    total_users = await Users.count_documents({})
    total_files = await file_collection.count_documents({})

    await message.reply_text(
        f"📈 **Bot Status Report**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👥 **Users Registered:** `{total_users}`\n"
        f"📦 **Files Stored:** `{total_files}`\n"
        f"⏳ **Uptime:** `{uptime}`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🤖 Bot is active and running smoothly!",
        disable_web_page_preview=True
    )