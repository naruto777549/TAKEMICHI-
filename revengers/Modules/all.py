from pyrogram import filters
from pyrogram.types import Message
from revengers import bot

@bot.on_message(filters.command(["all", ".all", "@all"]) & filters.group)
async def tag_all(bot, message: Message):
    # Check if sender is admin
    user_id = message.from_user.id
    chat_id = message.chat.id

    member = await bot.get_chat_member(chat_id, user_id)
    if member.status not in ["administrator", "creator"]:
        return await message.reply("🚫 Only group admins can use this command.")

    symbol = "➤"  # Customize symbol if needed

    # Fetch all chat members
    users = []
    async for member in bot.get_chat_members(chat_id):
        users.append(member.user)  # Include everyone

    if not users:
        return await message.reply("⚠️ No members found to tag.")

    # Optional custom message
    text = message.text.split(None, 1)
    custom_msg = text[1] if len(text) > 1 else None

    reply_to = message.reply_to_message.id if message.reply_to_message else None

    # Batch mentions (limit 5 per message to avoid flood)
    BATCH_SIZE = 5
    for i in range(0, len(users), BATCH_SIZE):
        mention_text = ""
        for user in users[i:i + BATCH_SIZE]:
            if user.username:
                mention = f"@{user.username}"
            else:
                mention = f"[{user.first_name}](tg://user?id={user.id})"
            mention_text += f"{symbol} {mention}\n"

        final_text = f"{custom_msg}\n\n{mention_text}" if custom_msg else mention_text
        await message.reply(final_text, reply_to_message_id=reply_to, disable_web_page_preview=True)