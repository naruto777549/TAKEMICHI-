from pyrogram import filters
from pyrogram.types import Message
from revengers.db import add_balance, reduce_balance, get_balance
from pyrogram.errors import PeerIdInvalid, UsernameNotOccupied
from revengers import bot

@bot.on_message(filters.command("give"))
async def give_coins(bot, message: Message):
    if message.reply_to_message and len(message.text.split()) == 2:
        try:
            amount = int(message.text.split()[1])
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username or message.reply_to_message.from_user.first_name
        except:
            return await message.reply("❌ <b>Invalid format.</b>\nReply to a user with: <code>/give 100</code>", quote=True)

    elif len(message.text.split()) == 3:
        try:
            username = message.text.split()[1].replace("@", "")
            amount = int(message.text.split()[2])
            user = await bot.get_users(username)
            user_id = user.id
        except:
            return await message.reply("❌ <b>Invalid username or amount.</b>\nUse: <code>/give @username 100</code>", quote=True)
    else:
        return await message.reply(
            "❌ <b>Incorrect format!</b>\n\n✅ Use:\n"
            "• <code>/give @username 100</code>\n"
            "• Or reply to a user with: <code>/give 100</code>",
            quote=True
        )

    sender_id = message.from_user.id
    sender_balance = get_balance(sender_id)

    if sender_balance < amount:
        return await message.reply("😕 <b>You don't have enough coins to give.</b>", quote=True)

    reduce_balance(sender_id, amount)
    add_balance(user_id, amount)
    new_balance = get_balance(user_id)

    await message.reply(
        f"🎁 <b>Coins Transferred!</b>\n\n"
        f"👤 <b>To:</b> <code>{username}</code>\n"
        f"💸 <b>Amount:</b> <code>{amount} coins</code>\n"
        f"📦 <b>New Balance:</b> <code>{new_balance} 🪙</code>",
        quote=True
    )