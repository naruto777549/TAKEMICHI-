from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Banned
from revengers.utils.checks import is_admin  # ✅ Admin check

# ✅ Helper to extract user from reply, @username, or user ID
async def extract_user_id(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name

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


@bot.on_message(filters.command("hardban") & filters.private)
async def hardban_user(bot, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You are not authorized to use this command.")

    user_id, user_name = await extract_user_id(message)

    if not user_id:
        return await message.reply("❌ Usage: `/hardban @username [reason]`, `/hardban user_id`, or reply to user.", quote=True)

    if await is_admin(user_id):
        return await message.reply("⚠️ You cannot ban another admin.", quote=True)

    if user_id in Banned:
        return await message.reply("⚠️ User is already hardbanned.", quote=True)

    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided"
    Banned.append(user_id)

    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"🚫 You have been *hardbanned* from using this bot.\n\n"
                 f"👮‍♂️ *Banned by:* `{message.from_user.first_name}` (`{message.from_user.id}`)\n"
                 f"📝 *Reason:* `{reason}`"
        )
    except:
        pass

    return await message.reply(
        f"✅ User `{user_id}` has been hardbanned.\n📝 Reason: `{reason}`", quote=True
    )


@bot.on_message(filters.command("unhardban") & filters.private)
async def unhardban_user(bot, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You are not authorized to use this command.")

    user_id, user_name = await extract_user_id(message)

    if not user_id:
        return await message.reply("❌ Usage: `/unhardban @username`, `/unhardban user_id`, or reply to user.", quote=True)

    if user_id not in Banned:
        return await message.reply("⚠️ User is not hardbanned.", quote=True)

    Banned.remove(user_id)

    try:
        await bot.send_message(chat_id=user_id, text="✅ You have been unhardbanned. You can now use the bot again.")
    except:
        pass

    return await message.reply(f"✅ User `{user_id}` has been unhardbanned.", quote=True)