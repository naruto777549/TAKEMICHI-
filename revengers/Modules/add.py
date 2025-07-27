from pyrogram import filters
from pyrogram.types import Message
from revengers.db import is_admin, add_chakra, get_user_chakra
from pyrogram.errors import PeerIdInvalid, UsernameNotOccupied

from revengers import bot  # bot = Client(...) ho to use this

@bot.on_message(filters.command("add") & filters.group)
async def add_chakra_cmd(bot, message: Message):
    sender = message.from_user
    if not await is_admin(sender.id):
        return await message.reply("🚫 Only <b>admins</b> can use this command.")

    if message.reply_to_message and len(message.command) == 2:
        try:
            target = message.reply_to_message.from_user
            amount = int(message.command[1])
        except ValueError:
            return await message.reply("❌ Invalid amount. Example: <code>/add 100</code>", parse_mode="HTML")
        
        await add_chakra(target.id, amount)
        new_total = await get_user_chakra(target.id)

        return await message.reply(
            f"✅ Successfully added 💠 <b>{amount}</b> chakra to <a href='tg://user?id={target.id}'>{target.first_name}</a>\n"
            f"⚡ New Total Chakra: <code>{new_total}</code>",
            parse_mode="HTML"
        )

    elif len(message.command) == 3:
        username = message.command[1].replace("@", "")
        try:
            user = await bot.get_users(username)
            amount = int(message.command[2])
        except (PeerIdInvalid, UsernameNotOccupied):
            return await message.reply("❌ Invalid username.")
        except ValueError:
            return await message.reply("❌ Invalid amount. Example: <code>/add @username 150</code>", parse_mode="HTML")
        
        await add_chakra(user.id, amount)
        new_total = await get_user_chakra(user.id)

        return await message.reply(
            f"✅ Successfully added 💠 <b>{amount}</b> chakra to <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
            f"⚡ New Total Chakra: <code>{new_total}</code>",
            parse_mode="HTML"
        )

    else:
        return await message.reply(
            "⚠️ Usage:\n"
            "<code>/add <amount></code> (reply to user)\n"
            "<code>/add @username <amount></code>",
            parse_mode="HTML"
        )
