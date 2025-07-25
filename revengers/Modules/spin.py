import random
from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import Users  # MongoDB Users collection

# Slot machine symbols
slots = ["🍒", "🍋", "🍉", "🍇", "⭐", "🍀"]

@bot.on_message(filters.command("spin") & filters.private)
async def spin_command(bot, message: Message):
    user_id = message.from_user.id
    user = await Users.find_one({"_id": user_id})

    # Check if user exists and has enough chakra
    if not user or user.get("chakra", 0) < 50:
        return await message.reply("❌ You need at least 50 Chakra Points to spin.")

    # Deduct 50 chakra for spin
    await Users.update_one({"_id": user_id}, {"$inc": {"chakra": -50}})

    # Perform the spin
    result = [random.choice(slots) for _ in range(3)]

    # Reward logic
    if len(set(result)) == 1:
        reward = 200  # All 3 match
    elif len(set(result)) == 2:
        reward = 100  # Any 2 match
    else:
        reward = random.randint(10, 50)  # No match, small reward

    # Add reward chakra
    await Users.update_one({"_id": user_id}, {"$inc": {"chakra": reward}})

    # Show result
    await message.reply(
        f"🎰 | {' | '.join(result)}\n\n"
        f"🎉 You won: {reward} Chakra Points!\n"
        f"💸 Spin cost: 50 Chakra"
    )