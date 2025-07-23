from pyrogram import filters
from pyrogram.types import Message
from revengers import bot

@bot.on_message(filters.command(["all", ".all", "@all"]) & filters.group)
async def tag_all(bot, message: Message):
    # Get list of all members from chat
    users = []
    async for member in bot.get_chat_members(message.chat.id):
        if not member.user.is_bot:
            users.append(member.user)

    if not users:
        return await message.reply("⚠️ No users found to tag.")

    # Prepare tag batches (5 users per message)
    text = message.text.split(None, 1)
    custom_msg = text[1] if len(text) > 1 else None

    reply_to = message.reply_to_message.id if message.reply_to_message else None

    BATCH_SIZE = 5
    for i in range(0, len(users), BATCH_SIZE):
        mention_text = ""
        for user in users[i:i + BATCH_SIZE]:
            mention_text += f"@{user.username} " if user.username else f"[{user.first_name}](tg://user?id={user.id}) "
        final_text = f"{custom_msg}\n\n{mention_text}" if custom_msg else mention_text
        await message.reply(final_text, reply_to_message_id=reply_to, disable_web_page_preview=True)