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

from pyrogram import filters
from pyrogram.types import Message
from revengers.db import add_balance, reduce_balance, get_balance
from revengers import bot  

@bot.on_message(filters.command("give") & filters.private)
async def give_coins(bot, message: Message):
    if message.reply_to_message and len(message.text.split()) == 2:
        # Reply-based transfer
        try:
            amount = int(message.text.split()[1])
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username or "user"
        except:
            return await message.reply("❌ Invalid format.\nUse: `/give <amount>` (as reply to a user)", quote=True)

    elif len(message.text.split()) == 3:
        # Username-based transfer
        try:
            username = message.text.split()[1].replace("@", "")
            amount = int(message.text.split()[2])
            user = await bot.get_users(username)
            user_id = user.id
        except:
            return await message.reply("❌ Invalid username or amount.\nUse: `/give @username <amount>`", quote=True)
    else:
        return await message.reply(
            "❌ Incorrect format.\n\n✅ Use:\n• `/give @username 100`\n• Or reply to a user: `/give 100`",
            quote=True
        )

    sender_id = message.from_user.id
    sender_balance = get_balance(sender_id)

    if sender_balance < amount:
        return await message.reply("😕 You don't have enough coins to give.", quote=True)

    reduce_balance(sender_id, amount)
    add_balance(user_id, amount)
    new_balance = get_balance(user_id)

    await message.reply(
        f"🎉 <b>Coins Transferred!</b>\n"
        f"👤 To: @{username}\n"
        f"💰 Amount: {amount} coins\n"
        f"📦 Their New Balance: {new_balance} 🪙",
        quote=True
    )
