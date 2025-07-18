from pyrogram import filters
from pyrogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from pyrogram.errors import UserNotParticipant
from revengers import bot
from revengers.db import file_collection, Users

CHANNELS = [
    ("https://t.me/Bey_war_updates", "ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ"),
    ("https://t.me/+ZyRZJntl2FU0NTk1", "sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ")
]


async def check_subscription(bot, message: Message):
    user_id = message.from_user.id
    for url, name in CHANNELS:
        try:
            chat = await bot.get_chat(url.split("/")[-1].replace("+", ""))
            member = await bot.get_chat_member(chat.id, user_id)
            if member.status in ("left", "kicked"):
                raise UserNotParticipant
        except:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton(name, url=url)] for url, name in CHANNELS
            ])
            await message.reply(
                f"›› ʜᴇʏ {message.from_user.mention} ×\n\n"
                "```#JOIN ALL CHANNEL\nʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ,\n"
                "sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs.```",
                reply_markup=buttons
            )
            return False
    return True


# Welcome video
async def send_start_video(bot, chat_id, mention):
    video_file_id = "BAACAgQAAxkBAAMHaHKBXy2VCMPrAAH8VcpV91M5lP9fAALnBwACiQ5tUWroh4Dwqk4rHgQ"
    caption = (
        f"🌟 {mention}, 𝕎𝕖𝕝𝕔𝕠𝕞𝕖 𝕥𝕠 𝕥𝕙𝕖 𝔽𝕚𝕝𝕖 𝕍𝕒𝕦𝕝𝕥!\n\n"
        "⚡ 𝕐𝕠𝕦𝕣 𝕦𝕝𝕥𝕚𝕞𝕒𝕥𝕖 𝕙𝕚𝕕𝕖𝕠𝕦𝕥 𝕗𝕠𝕣 𝕡𝕖𝕣𝕞𝕒𝕟𝕖𝕟𝕥 𝕗𝕚𝕝𝕖 𝕤𝕥𝕠𝕣𝕒𝕘𝕖!\n\n"
        "📂 𝕊𝕒𝕧𝕖 𝕗𝕚𝕝𝕖𝕤, 𝕘𝕣𝕒𝕓 𝕤𝕙𝕒𝕣𝕖𝕒𝕓𝕝𝕖 𝕝𝕚𝕟𝕜𝕤, 𝕒𝕟𝕕 𝕒𝕔𝕔𝕖𝕤𝕤 𝕥𝕙𝕖𝕞 𝕒𝕟𝕪𝕥𝕚𝕞𝕖.\n\n"
        "📥 𝔻𝕣𝕠𝕡 𝕒 𝕗𝕚𝕝𝕖 𝕥𝕠 𝕦𝕟𝕝𝕖𝕒𝕤𝕙 𝕥𝕙𝕖 𝕡𝕠𝕨𝕖𝕣 𝕠𝕣 𝕙𝕚𝕥 /help 𝕗𝕠𝕣 𝕥𝕙𝕖 𝕗𝕦𝕝𝕝 𝕟𝕚𝕟𝕛𝕒 𝕤𝕔𝕣𝕠𝕝𝕝! 🚀"
    )
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help_menu"),
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about_menu")
        ],
        [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ", url=CHANNELS[1][0])],
        [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=CHANNELS[0][0])]
    ])
    await bot.send_video(chat_id, video_file_id, caption=caption, reply_markup=buttons)


@bot.on_message(filters.command("start") & filters.private)
async def start_command(bot, message: Message):
    if not await check_subscription(bot, message):
        return

    user = message.from_user
    mention = user.mention

    await Users.update_one({"_id": user.id}, {"$set": {"name": user.first_name}}, upsert=True)

    args = message.text.split(maxsplit=1)
    if len(args) == 2:
        code = args[1]
        data = await file_collection.find_one({"code": code})
        if data:
            try:
                file_type = data.get("type", "document")
                file_id = data["file_id"]
                caption = data.get("caption") or "📦 𝗙𝗶𝗹𝗲 𝗳𝗿𝗼𝗺 𝗟𝗶𝗻𝗸"
                if file_type == "video":
                    return await message.reply_video(video=file_id, caption=caption)
                elif file_type == "photo":
                    return await message.reply_photo(photo=file_id, caption=caption)
                else:
                    return await message.reply_document(document=file_id, caption=caption)
            except Exception as e:
                return await message.reply(f"❌ Error sending file:\n<code>{e}</code>")
        return await message.reply("❗ Invalid or expired link.")

    await send_start_video(bot, message.chat.id, mention)