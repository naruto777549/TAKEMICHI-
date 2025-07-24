from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Banned
from config import ADMINS

# ✅ Check if user is admin
async def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

# ✅ Extract user ID from message
async def extract_user_id(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name

    if len(message.command) < 2:
        return None, None

    arg = message.command[1]

    if arg.startswith("@"):
        try:
            user = await bot.get_users(arg)
            return user.id, user.first_name
        except:
            return None, None

    if arg.isdigit():
        return int(arg), None

    return None, None

# ✅ Hardban command
@bot.on_message(filters.command("hardban") & filters.private)
async def hardban_user(bot, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You are not authorized to use this command.")

    user_id, user_name = await extract_user_id(message)
    if not user_id:
        return await message.reply("❌ Usage: `/hardban @username`, `/hardban user_id`, or reply to user.", quote=True)

    if await is_admin(user_id):
        return await message.reply("⚠️ You cannot ban another admin.", quote=True)

    # Check if already banned
    if await Banned.find_one({"_id": user_id}):
        return await message.reply("⚠️ User is already hardbanned.", quote=True)

    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided"

    # Add to banlist
    await Banned.insert_one({"_id": user_id, "reason": reason, "banned_by": message.from_user.id})

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

# ✅ Unhardban command
@bot.on_message(filters.command("unhardban") & filters.private)
async def unhardban_user(bot, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You are not authorized to use this command.")

    user_id, user_name = await extract_user_id(message)
    if not user_id:
        return await message.reply("❌ Usage: `/unhardban @username`, `/unhardban user_id`, or reply to user.", quote=True)

    if not await Banned.find_one({"_id": user_id}):
        return await message.reply("⚠️ User is not hardbanned.", quote=True)

    await Banned.delete_one({"_id": user_id})

    try:
        await bot.send_message(chat_id=user_id, text="✅ You have been unhardbanned. You can now use the bot again.")
    except:
        pass

    return await message.reply(f"✅ User `{user_id}` has been unhardbanned.", quote=True)