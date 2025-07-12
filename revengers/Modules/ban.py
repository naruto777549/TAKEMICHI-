from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Banned
from config import ADMINS


async def extract_user_id(message: Message):
    # 1. From reply
    if message.reply_to_message:
        return message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name

    # 2. From command args
    if len(message.command) < 2:
        return None, None

    arg = message.command[1]

    # Username format
    if arg.startswith("@"):
        try:
            user = await bot.get_users(arg)
            return user.id, user.first_name
        except:
            return None, None

    # Numeric ID format
    if arg.isdigit():
        return int(arg), None

    return None, None


@bot.on_message(filters.command("ban") & filters.private)
async def ban_user(bot, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("🚫 You are not authorized to use this command.")

    user_id, user_name = await extract_user_id(message)

    if not user_id:
        return await message.reply("❌ Usage: `/ban @username [reason]`, `/ban user_id`, or reply to user.", quote=True)

    if user_id in ADMINS:
        return await message.reply("⚠️ You cannot ban another admin.", quote=True)

    if user_id in Banned:
        return await message.reply("⚠️ User is already banned.", quote=True)

    # Extract reason if given
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided"

    # Add to ban list
    Banned.append(user_id)

    # Notify target user
    try:
        ban_msg = (
            "🚫 You have been *banned* from using this bot.\n\n"
            f"👮‍♂️ *Banned by:* `{message.from_user.first_name}` (`{message.from_user.id}`)\n"
            f"📝 *Reason:* `{reason}`"
        )
        await bot.send_message(chat_id=user_id, text=ban_msg)
    except:
        pass  # Ignore if user has not started the bot or is blocked

    return await message.reply(
        f"✅ User `{user_id}` has been banned.\n📝 Reason: `{reason}`",
        quote=True
    )


@bot.on_message(filters.command("unban") & filters.private)
async def unban_user(bot, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("🚫 You are not authorized to use this command.")

    user_id, user_name = await extract_user_id(message)

    if not user_id:
        return await message.reply("❌ Usage: `/unban @username`, `/unban user_id`, or reply to user.", quote=True)

    if user_id not in Banned:
        return await message.reply("⚠️ User is not banned.", quote=True)

    Banned.remove(user_id)

    # Optional: Notify user
    try:
        await bot.send_message(chat_id=user_id, text="✅ You have been unbanned. You can now use the bot again.")
    except:
        pass

    return await message.reply(f"✅ User `{user_id}` has been unbanned.", quote=True)