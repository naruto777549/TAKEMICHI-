from pyrogram import filters
from pyrogram.types import Message
from db import add_balance, reduce_balance, get_balance
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
