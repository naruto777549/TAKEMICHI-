from pyrogram import filters
from pyrogram.types import Message
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
    return await message.reply(f"✅ You received {DAILY_POINTS} Chakra Points today!")

# /bal — Check your Chakra balance
@bot.on_message(filters.command("bal") & filters.group)
async def chakra_balance(bot, message: Message):
    user_id = message.from_user.id
    balance = await get_user_chakra(user_id)
    return await message.reply(f"💠 Your Chakra Balance: `{balance} points`")

# Reward Chakra Points for saying "good" or "nice" in replies
@bot.on_message(filters.reply & filters.text & filters.group)
async def message_reward(bot, message: Message):
    if not re.search(r"\b(good|nice)\b", message.text.lower()):
        return

    sender = message.from_user
    receiver = message.reply_to_message.from_user

    if not receiver or receiver.is_bot or receiver.id == sender.id:
        return  # Ignore bot, self-reward

    await add_chakra(receiver.id, REWARD_POINTS)
    new_balance = await get_user_chakra(receiver.id)

    await message.reply(
        f"🌟 `{REWARD_POINTS}` Chakra Points awarded to [{receiver.first_name}](tg://user?id={receiver.id})!\n"
        f"💰 New Balance: `{new_balance} points`",
        quote=True
    )