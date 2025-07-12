from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Start command handler
@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    video_file_id = "AgAD5wcAAokObVE"  # Your saved video file_id

    caption = (
        "🌟 <b>Gᴏᴅ✘Nᴀʀᴜᴛᴏ File Vault!</b>\n\n"
        "⚡ <i>Your ultimate hideout for permanent file storage!</i>\n\n"
        "📂 Save files, grab shareable links, and access them anytime.\n\n"
        "📥 <b>Drop a file to unleash the power</b> or hit /help for the full ninja scroll! 🚀"
    )

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 Help", callback_data="help_menu"),
             InlineKeyboardButton("📚 About", callback_data="about_menu")],
            [InlineKeyboardButton("👥 Support Group", url="https://t.me/YourSupportGroupLink")],
            [InlineKeyboardButton("📢 Update Channel", url="https://t.me/YourUpdateChannelLink")]
        ]
    )

    await message.reply_video(
        video=video_file_id,
        caption=caption,
        reply_markup=buttons
    )