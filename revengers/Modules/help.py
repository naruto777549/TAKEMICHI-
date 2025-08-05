from pyrogram import filters
from pyrogram.types import Message
from revengers import bot

@bot.on_message(filters.command("help"))
async def help_cmd(_, message: Message):
    await message.reply(
        """★════════════════════➽
║ 🤖 𝗕𝗢𝗧 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦
★════════════════════➽
║ 🌀 /start - 𝗕𝗼𝘁 𝘀𝘁𝗮𝗿𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲
║ 📜 /help - 𝗦𝗵𝗼𝘄 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗹𝗶𝘀𝘁
║ 🗣 /tagall [msg] - 𝗧𝗮𝗴 𝗮𝗹𝗹 𝗴𝗿𝗼𝘂𝗽 𝗺𝗲𝗺𝗯𝗲𝗿𝘀
║ 🛑 /stoptag - 𝗦𝘁𝗼𝗽 𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝘁𝗮𝗴𝗴𝗶𝗻𝗴
║ 📢 /bcast - 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 (𝗢𝘄𝗻𝗲𝗿𝘀 𝗼𝗻𝗹𝘆)
★════════════════════➽"""
    )