from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.errors import PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from revengers import bot
from config import ADMINS
from revengers.db import Users, Banned

@bot.on_message(filters.command("bcast") & filters.private)
async def broadcast_handler(bot, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("🚫 You're not authorized to use this.")

    if not message.reply_to_message:
        return await message.reply("❗ Reply to a message (text/photo/video/document) to broadcast.")

    original = message.reply_to_message

    # Extract buttons if available
    keyboard = original.reply_markup if isinstance(original.reply_markup, InlineKeyboardMarkup) else None

    total = 0
    success = 0
    failed = 0
    blocked = 0

    async for user in Users.find():
        user_id = user["_id"]
        if user_id in Banned:
            continue

        total += 1

        try:
            if original.text:
                await bot.send_message(user_id, text=original.text, reply_markup=keyboard)
            elif original.photo:
                await bot.send_photo(user_id, photo=original.photo.file_id, caption=original.caption or "", reply_markup=keyboard)
            elif original.video:
                await bot.send_video(user_id, video=original.video.file_id, caption=original.caption or "", reply_markup=keyboard)
            elif original.document:
                await bot.send_document(user_id, document=original.document.file_id, caption=original.caption or "", reply_markup=keyboard)
            else:
                failed += 1
                continue
            success += 1

        except (UserIsBlocked, InputUserDeactivated, PeerIdInvalid):
            blocked += 1
            failed += 1
        except:
            failed += 1

    await message.reply(
        f"📢 **ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ**\n\n"
        f"👥 ᴛᴏᴛᴀʟ ᴜsᴇʀs: `{total}`\n"
        f"✅ ᴅᴇʟɪᴠᴇʀᴇᴅ: `{success}`\n"
        f"⛔ ʙʟᴏᴄᴋᴇᴅ: `{blocked}`\n"
        f"❌ ғᴀɪʟᴇᴅ: `{failed}`"
    )