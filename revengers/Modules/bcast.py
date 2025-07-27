from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.errors import PeerIdInvalid, UserIsBlocked, InputUserDeactivated, ChatWriteForbidden
from revengers import bot
from revengers.db import Users, Banned, get_all_groups
from revengers.utils.checks import is_admin
ADMIN = 7019600964

@bot.on_message(filters.command("broadcast") & filters.user(ADMIN))
async def broadcast_handler(_, msg: Message):
    if not msg.reply_to_message:
        return await msg.reply("📢 Please reply to a message to broadcast.")

    broadcast_msg = msg.reply_to_message

    m = await msg.reply("🚀 Broadcasting started...")

    success_users = 0
    failed_users = 0
    success_groups = 0
    failed_groups = 0

    users = await get_all_users()
    groups = await get_all_groups()

    total_users = len(users)
    total_groups = len(groups)

    await m.edit(
        f"📢 Starting Broadcast...\n\n👤 Users: {total_users} | 👥 Groups: {total_groups}"
    )

    # 🔹 Send to users
    for user in users:
        user_id = user["_id"]
        try:
            await broadcast_msg.copy(chat_id=user_id)
            success_users += 1
        except Exception:
            failed_users += 1
        await asyncio.sleep(0.05)

    # 🔹 Send to groups
    for group in groups:
        group_id = group["_id"]
        try:
            await broadcast_msg.copy(chat_id=group_id)
            success_groups += 1
        except Exception:
            failed_groups += 1
        await asyncio.sleep(0.05)

    await m.edit(
        f"✅ Broadcast Finished!\n\n"
        f"👤 Users:\n   ✅ {success_users} | ❌ {failed_users}\n"
        f"👥 Groups:\n   ✅ {success_groups} | ❌ {failed_groups}"
    )

