from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from revengers import bot

@bot.on_message(filters.command("start") & filters.private)
async def start_command(bot, message: Message):
    user = message.from_user.mention
    video_file_id = "BAACAgQAAxkBAAIBM2hye06wZl3COnMo4IdT3aIBsLjIAALnBwACiQ5tUQLmNmLJk2bTHgQ"

    caption = (
        f"🌟 {user}, 𝕎𝕖𝕝𝕔𝕠𝕞𝕖 𝕥𝕠 𝕥𝕙𝕖 𝔽𝕚𝕝𝕖 𝕍𝕒𝕦𝕝𝕥!\n\n"
        "⚡ 𝕐𝕠𝕦𝕣 𝕦𝕝𝕥𝕚𝕞𝕒𝕥𝕖 𝕙𝕚𝕕𝕖𝕠𝕦𝕥 𝕗𝕠𝕣 𝕡𝕖𝕣𝕞𝕒𝕟𝕖𝕟𝕥 𝕗𝕚𝕝𝕖 𝕤𝕥𝕠𝕣𝕒𝕘𝕖!\n\n"
        "📂 𝕊𝕒𝕧𝕖 𝕗𝕚𝕝𝕖𝕤, 𝕘𝕣𝕒𝕓 𝕤𝕙𝕒𝕣𝕖𝕒𝕓𝕝𝕖 𝕝𝕚𝕟𝕜𝕤, 𝕒𝕟𝕕 𝕒𝕔𝕔𝕖𝕤𝕤 𝕥𝕙𝕖𝕞 𝕒𝕟𝕪𝕥𝕚𝕞𝕖.\n\n"
        "📥 𝔻𝕣𝕠𝕡 𝕒 𝕗𝕚𝕝𝕖 𝕥𝕠 𝕦𝕟𝕝𝕖𝕒𝕤𝕙 𝕥𝕙𝕖 𝕡𝕠𝕨𝕖𝕣 𝕠𝕣 𝕙𝕚𝕥 /𝕙𝕖𝕝𝕡 𝕗𝕠𝕣 𝕥𝕙𝕖 𝕗𝕦𝕝𝕝 𝕟𝕚𝕟𝕛𝕒 𝕤𝕔𝕣𝕠𝕝𝕝! 🚀"
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