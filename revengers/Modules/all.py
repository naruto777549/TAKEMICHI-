from pyrogram import filters
from pyrogram.types import Message
from revengers import bot

@bot.on_message(filters.command("all", prefixes=["/", "@", "~", "."]) & filters.group)
async def tag_all(bot, message: Message):
    symbol = "➤"  # Customize this symbol

    # Get all members
    users = []
    async for member in bot.get_chat_members(message.chat.id):
        users.append(member.user)

    if not users:
        return await message.reply("⚠️ No members found to tag.")

    # Determine custom message and reply context
    parts = message.text.split(None, 1)
    custom_msg = parts[1] if len(parts) > 1 else None
    replied_text = message.reply_to_message.text if message.reply_to_message else None

    # Final reason/message to use
    reason = ""
    if replied_text and custom_msg:
        reason = f"💬 {custom_msg}\n🔁 <i>{replied_text}</i>"
    elif replied_text:
        reason = f"🔁 <i>{replied_text}</i>"
    elif custom_msg:
        reason = f"💬 {custom_msg}"

    # Mention users in batches
    BATCH_SIZE = 5
    reply_to = message.reply_to_message.id if message.reply_to_message else None

    for i in range(0, len(users), BATCH_SIZE):
        mentions = ""
        for user in users[i:i + BATCH_SIZE]:
            name = user.first_name.replace("[", "").replace("]", "")
            mention = f"[{name}](tg://user?id={user.id})"
            mentions += f"{symbol} {mention}\n"

        final_text = f"{reason}\n\n{mentions}" if reason else mentions
        await message.reply(final_text, reply_to_message_id=reply_to, disable_web_page_preview=True)