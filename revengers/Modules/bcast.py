import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import (
    PeerIdInvalid,
    UserIsBlocked,
    InputUserDeactivated,
    ChatWriteForbidden,
)

from revengers import bot
from revengers.db import Users, Groups, add_group, is_admin, is_banned, get_all_groups

ADMIN = 7576729648  # Replace with your Telegram user ID


async def get_all_users():
    return [user async for user in Users.find({})]


@bot.on_message(filters.command("broadcast") & filters.user(ADMIN))
async def broadcast_handler(_, msg: Message):
    if not msg.reply_to_message:
        return await msg.reply("📢 Reply to a message to broadcast.")

    broadcast_msg = msg.reply_to_message
    status = await msg.reply("🚀 Broadcasting started...")

    success_users = failed_users = success_groups = failed_groups = 0
    users = await get_all_users()
    groups = await get_all_groups()

    await status.edit_text(
        f"📢 Starting Broadcast...\n👤 Users: {len(users)} | 👥 Groups: {len(groups)}"
    )

    # Broadcast to Users
    for user in users:
        user_id = user["_id"]
        if await is_banned(user_id):
            continue
        try:
            await broadcast_msg.copy(chat_id=user_id)
            success_users += 1
        except (PeerIdInvalid, UserIsBlocked, InputUserDeactivated, ChatWriteForbidden):
            failed_users += 1
        except Exception:
            failed_users += 1
        await asyncio.sleep(0.05)

    # Broadcast to Groups
    for group in groups:
        group_id = group["_id"]
        if await is_banned(group_id):
            continue
        try:
            await broadcast_msg.copy(chat_id=group_id)
            success_groups += 1
        except (PeerIdInvalid, ChatWriteForbidden):
            failed_groups += 1
        except Exception:
            failed_groups += 1
        await asyncio.sleep(0.05)

    await status.edit_text(
        f"✅ **Broadcast Completed!**\n\n"
        f"👤 Users:\n   ✅ {success_users} | ❌ {failed_users}\n"
        f"👥 Groups:\n   ✅ {success_groups} | ❌ {failed_groups}"
    )


# ✅ Save group automatically when /start is used in a group
@bot.on_message(filters.command("start") & filters.group)
async def save_group_on_command(_, msg: Message):
    group_id = msg.chat.id
    group_title = msg.chat.title or "Unnamed"
    await add_group(group_id, group_title)
    await msg.reply_text("✅ This group has been saved in the database.")
