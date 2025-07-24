import time
import psutil
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
from revengers import bot, start_time  # make sure start_time = datetime.utcnow() is in __init__.py or main.py

def get_uptime():
    uptime = datetime.utcnow() - start_time
    seconds = int(uptime.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}ʜ:{minutes}ᴍ:{seconds}s"

@bot.on_message(filters.command("ping"))
async def ping_handler(bot, message: Message):
    start = time.time()
    reply = await message.reply("🔍")
    ping_ms = (time.time() - start) * 1000

    ram_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()
    disk_usage = psutil.disk_usage("/").percent

    await reply.edit_text(
        f"➻ ᴩᴏɴɢ : `{ping_ms:.3f}`ᴍs\n\n"
        f"**{bot.me.first_name} sʏsᴛᴇᴍ sᴛᴀᴛs :**\n\n"
        f"๏ ᴜᴩᴛɪᴍᴇ : `{get_uptime()}`\n"
        f"๏ ʀᴀᴍ : `{ram_usage}%`\n"
        f"๏ ᴄᴩᴜ : `{cpu_usage}%`\n"
        f"๏ ᴅɪsᴋ : `{disk_usage}%`"
    )