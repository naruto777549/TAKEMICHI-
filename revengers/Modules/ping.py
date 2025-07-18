import time
from pyrogram import filters
from pyrogram.types import Message
from revengers import bot

@bot.on_message(filters.command("ping") & filters.private)
async def ping_handler(bot, message: Message):
    start = time.time()
    reply = await message.reply("🏓 Pinging...")
    end = time.time()

    ping_time = int((end - start) * 1000)  # in ms

    await reply.edit_text(
        f"🏓 𝗣𝗼𝗻𝗴! `{ping_time}ms`\n\n"
        "✅ 𝗕𝗼𝘁 𝗶𝘀 𝗮𝗹𝗶𝘃𝗲 & 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗶𝗻𝗴.",
        disable_web_page_preview=True
    )