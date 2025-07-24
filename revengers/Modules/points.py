from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from revengers import bot
from revengers.db import (
    chakra_users,
    get_user_chakra,
    add_chakra,
    can_claim_daily,
    claim_daily
)
from datetime import datetime
import re

DAILY_POINTS = 100
REWARD_POINTS = 25

# /daily — Claim Chakra Points daily
@bot.on_message(filters.command("daily") & filters.group)
async def daily_points(bot, message: Message):
    user_id = message.from_user.id
    if not await can_claim_daily(user_id):
        return await message.reply("⏳ You already claimed your daily Chakra. Try again tomorrow.")

    await claim_daily(user_id, DAILY_POINTS)
    new_balance = await get_user_chakra(user_id)

    text = f"""🎁 <b>Daily Bonus:</b> You received <code>{DAILY_POINTS:,}</code> Chakra!
💰 <b>New Balance:</b> <code>{new_balance:,}</code>"""

    return await message.reply(text, parse_mode=ParseMode.HTML)

# /bal — Check your Chakra balance
@bot.on_message(filters.command("bal") & filters.group)
async def chakra_balance(bot, message: Message):
    user = message.from_user
    user_id = user.id
    balance = await get_user_chakra(user_id)

    text = f"""✨ <b>Balance Check</b>

👤 <b>User:</b> {user.mention}
💠 <b>Chakra:</b> <code>{balance:,} points</code>
"""
    await message.reply(text, parse_mode=ParseMode.HTML)

# Reward Chakra Points for saying "good" or "nice" in replies
@bot.on_message(filters.reply & filters.text & filters.group)
async def message_reward(bot, message: Message):
    if not re.search(r"\b(good|nice)\b", message.text.lower()):
        return

    sender = message.from_user
    receiver = message.reply_to_message.from_user

    if not receiver or receiver.is_bot or receiver.id == sender.id:
        return  # Ignore bot or self-reward

    await add_chakra(receiver.id, REWARD_POINTS)
    new_balance = await get_user_chakra(receiver.id)

    await message.reply(
        f"🌟 <b>{REWARD_POINTS} Chakra Points</b> awarded to <a href='tg://user?id={receiver.id}'>{receiver.first_name}</a>!\n"
        f"💠 <b>New Balance:</b> <code>{new_balance} points</code>",
        parse_mode=ParseMode.HTML
    )

@bot.on_message(filters.command("rank") & filters.group)
async def top_chakra(bot, message: Message):
    top_users = await get_top_chakra()

    if not top_users:
        return await message.reply("⚠️ No Chakra holders found.")

    text = "🏆 **Top Chakra Holders**\n\n"
    for idx, user in enumerate(top_users, start=1):
        user_id = user["_id"]
        chakra = user.get("chakra", 0)

        try:
            user_info = await bot.get_users(user_id)
            name = user_info.first_name
        except:
            name = "Unknown"

        text += f"🔹 {idx}. [{name}](tg://user?id={user_id}) — `{chakra:,}` Chakra\n"

    await message.reply(text, quote=True)