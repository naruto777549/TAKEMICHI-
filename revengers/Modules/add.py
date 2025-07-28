from pyrogram import filters
from pyrogram.types import Message
from revengers.db import add_balance, get_user_chakra
from revengers import bot

@bot.on_message(filters.command("add") & filters.group)
async def add_chakra_points(bot, message: Message):
    if message.reply_to_message and len(message.text.split()) == 2:
        try:
            amount = int(message.text.split()[1])
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username or "user"
        except:
            return await message.reply("❌ Invalid format.\nUse: `/add <amount>` (as a reply to a user)", quote=True)

    elif len(message.text.split()) == 3:
        try:
            username = message.text.split()[1].replace("@", "")
            amount = int(message.text.split()[2])
            user = await bot.get_users(username)
            user_id = user.id
        except:
            return await message.reply("❌ Invalid username or amount.\nUse: `/add @username <amount>`", quote=True)
    else:
        return await message.reply(
            "❌ Incorrect format.\n\n✅ Use:\n• `/add @username 100`\n• Or reply to a user: `/add 100`",
            quote=True
        )

    await add_balance(user_id, amount)
    current_chakra = await get_user_chakra(user_id)

    await message.reply(
        f"✅ <b>Chakra Points Added Successfully!</b>\n\n"
        f"👤 <b>User:</b> @{username}\n"
        f"🔮 <b>Chakra Points Added:</b> <code>{amount}</code>\n"
        f"🌟 <b>Total Chakra Points:</b> <code>{current_chakra}</code>",
        quote=True
    )