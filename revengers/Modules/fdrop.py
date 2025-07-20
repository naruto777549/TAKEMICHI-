from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from revengers import bot
from revengers.db import waifu_collection

OWNER_ID = 7576729648  # Replace with your actual ID

@bot.on_message(filters.command("fdrop") & filters.group)
async def fdrop_command(bot, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ Only the bot owner can use this command.")

    waifu = await waifu_collection.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
    if not waifu:
        return await message.reply("⚠️ No waifus in the database.")

    waifu = waifu[0]
    await message.reply_photo(
        photo=waifu["image"],
        caption="🎀 *Guess this waifu!*\n\nReply with `/guess <name>`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Hint 💡", callback_data="waifu_hint")]
        ])
    )