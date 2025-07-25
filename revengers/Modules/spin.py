import random
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import get_user_chakra, add_chakra, chakra_users

@bot.on_message(filters.command("spin") & filters.group)
async def spin_command(bot, message: Message):
    user = message.from_user
    user_id = user.id

    # Check chakra balance
    chakra = await get_user_chakra(user_id)
    if chakra < 50:
        return await message.reply(
            f"❌ You need at least 50 Chakra Points to spin.\nCurrent Balance: `{chakra}`"
        )

    # Deduct chakra for spin
    await chakra_users.update_one(
        {"_id": user_id}, {"$inc": {"chakra": -50}}, upsert=True
    )

    # Initial spinning animation
    spinning_msg = await message.reply("🎰 Spinning...")
    await asyncio.sleep(1.5)

    # Slot machine logic
    slots = ["🍒", "🍋", "🍉", "🍇", "⭐", "🍀"]
    result = [random.choice(slots) for _ in range(3)]

    # Calculate reward
    if result[0] == result[1] == result[2]:
        reward = 200
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        reward = 100
    else:
        reward = random.randint(10, 50)

    # Add reward chakra
    await add_chakra(user_id, reward)

    # Final result message
    await spinning_msg.edit_text(
        f"🎰 | {' | '.join(result)} | 🎰\n\n"
        f"🏆 You won: `{reward}` Chakra Points!\n"
        f"💸 Spin Cost: `50`\n"
        f"🪙 New Balance: `{chakra - 50 + reward}`"
    )