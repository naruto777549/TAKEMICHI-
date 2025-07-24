from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

from revengers import bot
from revengers.db import Users, file_collection

# 🔐 Channel for forced subscription
CHANNELS = [("Bey_war_updates", "ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ")]

# ✅ Check if user is subscribed to the update channel
async def check_subscription(bot, message: Message) -> bool:
    if message.chat.type != "private":
        return True  # No check in groups

    user_id = message.from_user.id
    channel_username, channel_name = CHANNELS[0]

    try:
        member = await bot.get_chat_member(channel_username, user_id)
        if member.status in ("left", "kicked"):
            raise UserNotParticipant
    except Exception:
        button = InlineKeyboardMarkup([
            [InlineKeyboardButton(channel_name, url=f"https://t.me/{channel_username}")]
        ])
        await message.reply(
            f"›› ʜᴇʏ {message.from_user.mention} ×\n\n"
            "```#JOIN CHANNEL\nʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ,\n"
            "sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs.```",
            reply_markup=button
        )
        return False
    return True

# ✅ Welcome/start video with inline buttons
async def send_start_video(bot, chat_id: int, mention: str):
    video_file_id = "BAACAgQAAxkBAAMHaHKBXy2VCMPrAAH8VcpV91M5lP9fAALnBwACiQ5tUWroh4Dwqk4rHgQ"
    caption = (
        f"🌟 {mention}, 𝕎𝕖𝕝𝕔𝕠𝕞𝕖 𝕥𝕠 𝕥𝕙𝕖 𝔽𝕚𝕝𝕖 𝕍𝕒𝕦𝕝𝕥!\n\n"
        "⚡ 𝕐𝕠𝕦𝕣 𝕦𝕝𝕥𝕚𝕞𝕒𝕥𝕖 𝕙𝕚𝕕𝕖𝕠𝕦𝕥 𝕗𝕠𝕣 𝕡𝕖𝕣𝕞𝕒𝕟𝕖𝕟𝕥 𝕗𝕚𝕝𝕖 𝕤𝕥𝕠𝕣𝕒𝕘𝕖!\n\n"
        "📂 𝕊𝕒𝕧𝕖 𝕗𝕚𝕝𝕖𝕤, 𝕘𝕖𝕥 𝕤𝕙𝕒𝕣𝕖𝕒𝕓𝕝𝕖 𝕝𝕚𝕟𝕜𝕤, 𝕒𝕟𝕕 𝕒𝕔𝕔𝕖𝕤𝕤 𝕥𝕙𝕖𝕞 𝕒𝕟𝕪𝕥𝕚𝕞𝕖.\n\n"
        "📥 𝔻𝕣𝕠𝕡 𝕒 𝕗𝕚𝕝𝕖 𝕥𝕠 𝕤𝕥𝕠𝕣𝕖 𝕠𝕣 𝕥𝕪𝕡𝕖 /help 𝕥𝕠 𝕤𝕖𝕖 𝕠𝕡𝕥𝕚𝕠𝕟𝕤 🚀"
    )
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help_menu"),
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about_menu")
        ],
        [InlineKeyboardButton(CHANNELS[0][1], url=f"https://t.me/{CHANNELS[0][0]}")]
    ])
    await bot.send_video(chat_id, video_file_id, caption=caption, reply_markup=buttons)

# ✅ Main /start command
@bot.on_message(filters.command("start"))
async def start_command(bot, message: Message):
    if message.chat.type == "private":
        if not await check_subscription(bot, message):
            return

        await Users.update_one(
            {"_id": message.from_user.id},
            {"$set": {"name": message.from_user.first_name}},
            upsert=True
        )

    args = message.text.split(maxsplit=1)
    if len(args) == 2:
        code = args[1].strip()
        data = await file_collection.find_one({"code": code})
        if data:
            try:
                file_id = data["file_id"]
                caption = data.get("caption") or "📦 𝗙𝗶𝗹𝗲 𝗳𝗿𝗼𝗺 𝗟𝗶𝗻𝗸"
                file_type = data.get("type", "document")
                if file_type == "video":
                    return await message.reply_video(file_id, caption=caption)
                elif file_type == "photo":
                    return await message.reply_photo(file_id, caption=caption)
                else:
                    return await message.reply_document(file_id, caption=caption)
            except Exception as e:
                return await message.reply(f"❌ Error sending file:\n<code>{e}</code>")
        else:
            return await message.reply("❗ Invalid or expired link.")

    # Default welcome message
    await send_start_video(bot, message.chat.id, message.from_user.mention)