from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import add_balance, reduce_balance, get_balance

@bot.on_message(filters.command("give") & (filters.group | filters.private))
async def give_chakra(bot, message: Message):
    if message.reply_to_message and len(message.text.split()) == 2:
        try:
            amount = int(message.text.split()[1])
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username or "user"
        except Exception:
            return await message.reply(
                "❌ <b>Invalid format.</b>\nUse: <code>/give &lt;amount&gt;</code> (as reply to a user)",
                quote=True
            )

    elif len(message.text.split()) == 3:
        try:
            username = message.text.split()[1].replace("@", "")
            amount = int(message.text.split()[2])
            user = await bot.get_users(username)
            user_id = user.id
        except Exception:
            return await message.reply(
                "❌ <b>Invalid username or amount.</b>\nUse: <code>/give @username &lt;amount&gt;</code>",
                quote=True
            )

    else:
        return await message.reply(
            "❌ <b>Incorrect format.</b>\n\n"
            "✅ <b>Correct Usage:</b>\n"
            "• <code>/give @username 100</code>\n"
            "• Or reply to a user with: <code>/give 100</code>",
            quote=True
        )

    sender_id = message.from_user.id
    sender_balance = await get_balance(sender_id)

    if sender_balance < amount:
        return await message.reply(
            "😕 <b>You don’t have enough chakra points.</b>\n"
            f"💼 <b>Your Balance:</b> <code>{sender_balance} 🔮</code>",
            quote=True
        )

    await reduce_balance(sender_id, amount)
    await add_balance(user_id, amount)
    new_balance = await get_balance(user_id)

    await message.reply(
        f"🎁 <b>Chakra Points Sent Successfully!</b>\n\n"
        f"👤 <b>To:</b> @{username}\n"
        f"💸 <b>Amount:</b> <code>{amount} 🔮</code>\n"
        f"💼 <b>Receiver's Balance:</b> <code>{new_balance} 🔮</code>",
        quote=True
    )