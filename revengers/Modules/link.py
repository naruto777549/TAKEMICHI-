from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from config import ADMINS

@bot.on_message(filters.command("link") & filters.private)
async def link_command(bot, message: Message):
    # Check if user is an admin
    if message.from_user.id not in ADMINS:
        return  # silently ignore

    # Check if replying to a message with a file
    if not message.reply_to_message or not (
        message.reply_to_message.video or message.reply_to_message.document
    ):
        return await message.reply("❗ Reply to a video or file with /link to generate a download command.")

    media = message.reply_to_message.video or message.reply_to_message.document
    file_id = media.file_id
    file_name = media.file_name if getattr(media, "file_name", None) else "Unnamed"
    file_size = round(media.file_size / 1024 / 1024, 2)

    text = (
        f"📁 <b>File:</b> <code>{file_name}</code>\n"
        f"📦 <b>Size:</b> {file_size} MB\n"
        f"🔗 <b>Command:</b>\n<code>/get {file_id}</code>"
    )

    await message.reply(text)