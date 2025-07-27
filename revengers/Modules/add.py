from pyrogram import filters
from pyrogram.types import Message
from revengers.db import is_admin, add_chakra, get_user_chakra
from pyrogram.errors import PeerIdInvalid, UsernameNotOccupied
from revengers import bot
import html

@bot.on_message(filters.command("add") & filters.group)
async def add_chakra_cmd(bot, message: Message):
    sender = message.from_user

    if not await is_admin(sender.id):
        return await message.reply("🚫 Only admins can use this command.")

    # ✅ Reply: /add <amount>
    if message.reply_to_message and len(message.command) == 2:
        try:
            target = message.reply_to_message.from_user
            if not target:
                return await message.reply("❌ Cannot identify the replied user.")
            amount = int(message.command[1])
        except ValueError:
            return await message.reply("❌ Invalid amount. Example: /add 100")

        await add_chakra(target.id, amount)
        new_total = await get_user_chakra(target.id)

        safe_name = html.escape(target.first_name or "User")
        return await message.reply(
            f"✅ Successfully added 💠 {amount} chakra to {safe_name} (ID: <code>{target.id}</code>)\n"
            f"⚡ New Total Chakra: <code>{new_total}</code>"
        )

    # ✅ Without reply: /add @username <amount>
    elif len(message.command) == 3:
        username = message.command[1].replace("@", "")
        try:
            user = await bot.get_users(username)
            amount = int(message.command[2])
        except (PeerIdInvalid, UsernameNotOccupied):
            return await message.reply("❌ Invalid username.")
        except ValueError:
            return await message.reply("❌ Invalid amount. Example: /add @username 150")

        await add_chakra(user.id, amount)
        new_total = await get_user_chakra(user.id)

        safe_name = html.escape(user.first_name or "User")
        return await message.reply(
            f"✅ Successfully added 💠 {amount} chakra to {safe_name} (ID: <code>{user.id}</code>)\n"
            f"⚡ New Total Chakra: <code>{new_total}</code>"
        )

    # ⚠️ Wrong usage
    return await message.reply(
        "⚠️ Usage:\n"
        "/add <amount> (reply to user)\n"
        "/add @username <amount>"
    )
