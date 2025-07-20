from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType, ParseMode
from revengers import bot
from revengers.db import waifu_collection

OWNER_ID = 7576729648  # Your Telegram user ID

@bot.on_message(filters.command("fdrop") & filters.private)
async def fdrop_all_groups(bot, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ Only the bot owner can use this command.")

    waifu = await waifu_collection.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
    if not waifu:
        return await message.reply("⚠️ No waifus in the database.")

    waifu = waifu[0]
    caption = (
        "🎀 *A mysterious waifu appears!*\n\n"
        "💭 Can you guess who she is?\n"
        "⤷ Reply with `/guess <name>` to try your luck!"
    )

    # Get all group chats the bot is part of
    async for dialog in bot.get_dialogs():
        if dialog.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            try:
                await bot.send_photo(
                    chat_id=dialog.chat.id,
                    photo=waifu["image"],
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                print(f"Failed to send to {dialog.chat.title} — {e}")

    await message.reply("✅ Waifu dropped in all groups.")