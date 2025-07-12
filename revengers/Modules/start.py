from pyrogram import filters
from pyrogram.types import Message
from revengers import bot

@bot.on_message(filters.command("link") & filters.private)
async def link_command(bot, message: Message):
    if not message.reply_to_message or not (message.reply_to_message.video or message.reply_to_message.document):
        return await message.reply("❗ Reply to a video or file with /link to generate a download link.")

    media = message.reply_to_message.video or message.reply_to_message.document
    file_id = media.file_id
    file_name = media.file_name if hasattr(media, 'file_name') and media.file_name else "Unnamed"
    file_size = round(media.file_size / 1024 / 1024, 2)

    # Build your link using file_id — the actual implementation depends on how you're serving files
    # For Pyrogram bots, you typically can't share direct links unless you host files somewhere
    # But we can send back a command that uses file_id again (for internal bot use)
    response = (
        f"🎬 <b>File Name:</b> <code>{file_name}</code>\n"
        f"📦 <b>Size:</b> {file_size} MB\n"
        f"🔗 <b>Sharable Command:</b>\n"
        f"<code>/get {file_id}</code>\n\n"
        f"✨ Use this command to regenerate this file anytime!"
    )

    await message.reply(response)