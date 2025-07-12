from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from revengers import bot  

@bot.on_message(filters.command("start") & filters.private)
async def start_command(bot, message: Message):
    video_file_id = "AgAD5wcAAokObVE"  # Your saved video file_id
    user = message.from_user.mention  # mention format: clickable user

    caption = (
        f"🌟 <b>{user}, Welcome to the File Vault!</b>\n\n"
        "⚡ <i>Your ultimate hideout for permanent file storage!</i>\n\n"
        "📂 Save files, grab shareable links, and access them anytime.\n\n"
        "📥 <b>Drop a file to unleash the power</b> or hit /help for the full ninja scroll! 🚀"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📜 Help", callback_data="help_menu"),
                InlineKeyboardButton("📚 About", callback_data="about_menu")
            ],
            [
                InlineKeyboardButton("👥 Support Group", url="https://t.me/YourSupportGroupLink")
            ],
            [
                InlineKeyboardButton("📢 Update Channel", url="https://t.me/YourUpdateChannelLink")
            ]
        ]
    )

    await message.reply_video(
        video=video_file_id,
        caption=caption,
        reply_markup=buttons
    )