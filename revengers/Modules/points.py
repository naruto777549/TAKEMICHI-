from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import ChakraPoints
from datetime import datetime, timedelta
import re

# How many points for daily and messages
DAILY_POINTS = 20
REWARD_POINTS = 5

# Utility to fetch or create user data
async def get_user_points(user_id):
    user = await ChakraPoints.find_one({"_id": user_id})
    if not user:
        await ChakraPoints.insert_one({"_id": user_id, "points": 0, "last_daily": None})
        return {"_id": user_id, "points": 0, "last_daily": None}
    return user

# /daily command
@bot.on_message(filters.command("daily") & filters.group)
async def daily_points(bot, message: Message):
    user_id = message.from_user.id
    user = await get_user_points(user_id)

    now = datetime.utcnow()
    if user.get("last_daily") and now - user["last_daily"] < timedelta(hours=24):
        remaining = timedelta(hours=24) - (now - user["last_daily"])
        return await message.reply(f"⏳ You already claimed daily. Try again in {remaining.seconds//3600}h {(remaining.seconds//60)%60}m.")

    await ChakraPoints.update_one({"_id": user_id}, {
        "$inc": {"points": DAILY_POINTS},
        "$set": {"last_daily": now}
    })
    await message.reply(f"✅ You received {DAILY_POINTS} Chakra Points as daily reward!")

# /bal command
@bot.on_message(filters.command("bal") & filters.group)
async def check_balance(bot, message: Message):
    user_id = message.from_user.id
    user = await get_user_points(user_id)
    await message.reply(f"💠 Your Chakra Balance: `{user['points']} points`")

# Detect "good" or "nice" in reply
@bot.on_message(filters.reply & filters.text & filters.group)
async def message_reward(bot, message: Message):
    if not re.search(r"\b(good|nice)\b", message.text.lower()):
        return

    sender_id = message.from_user.id
    receiver = message.reply_to_message.from_user

    if not receiver or receiver.is_bot or receiver.id == sender_id:
        return  # Ignore self or bot

    await get_user_points(receiver.id)

    await ChakraPoints.update_one({"_id": receiver.id}, {
        "$inc": {"points": REWARD_POINTS}
    })

    new_data = await ChakraPoints.find_one({"_id": receiver.id})
    await message.reply(
        f"🌟 `{REWARD_POINTS}` Chakra Points awarded to [{receiver.first_name}](tg://user?id={receiver.id})!\n"
        f"💰 New Balance: `{new_data['points']} points`",
        quote=True
    )