import time
import psutil
import platform
from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import get_total_users, get_total_groups

@bot.on_message(filters.command("ping"))
async def ping_command(_, message: Message):
    start = time.time()
    sent_msg = await message.reply("🔍")
    end = time.time()

    ping = round((end - start) * 1000)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    total, used, free = map(lambda x: round(x / (1024 ** 3), 2), psutil.virtual_memory()[:3])

    total_users = await get_total_users()
    total_groups = await get_total_groups()

    await sent_msg.edit(
        f"""🏓 ᴘᴏɴɢ! ʙᴏᴛ ɪs ᴀʟɪᴠᴇ!

╭──[ 𝙎𝙔𝙎𝙏𝙀𝙈 𝙎𝙏𝘼𝙏𝙎 ]
├ 🧠 ʀᴀᴍ: {ram}% ᴜsᴇᴅ
├ 💾 ᴛᴏᴛᴀʟ ʀᴀᴍ: {total} GB
├ ⚙️ ᴄᴘᴜ: {cpu}%
├ 📡 ᴘɪɴɢ: {ping} ms
╰───────

╭──[ ᴛᴀɢᴀʟʟ ʙᴏᴛ ]
├ 👥 ᴛᴏᴛᴀʟ ᴜsᴇʀs: {total_users}
├ 🏘️ ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs: {total_groups}
╰─────────────""",
        disable_web_page_preview=True
    )