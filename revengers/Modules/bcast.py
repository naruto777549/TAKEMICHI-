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
from revengers.db import Users, Banned, get_all_groups, add_group, remove_group, is_admin

ADMIN = 7576729648  # Set your Telegram user ID


async def get_all_users():
    return [user async for user in Users.find({}) if user["_id"] not in Banned]


@bot.on_message(filters.command("broadcast") & filters.user(ADMIN))
async def broadcast_handler(_, msg: Message):
    if not msg.reply_to_message:
        return await msg.reply("📢 Please reply to a message to broadcast.")

    broadcast_msg = msg.reply_to_message
    m = await msg.reply("🚀 Broadcasting started...")

    success_users = failed_users = success_groups = failed_groups = 0
    users = await get_all_users()
    groups = await get_all_groups()

    await m.edit(
        f"📢 Starting Broadcast...\n\n👤 Users: {len(users)} | 👥 Groups: {len(groups)}"
    )

    # Broadcasting to Users
    for user in users:
        user_id = user["_id"]
        try:
            await broadcast_msg.copy(chat_id=user_id)
            success_users += 1
        except (PeerIdInvalid, UserIsBlocked, InputUserDeactivated, ChatWriteForbidden):
            failed_users += 1
        except Exception:
            failed_users += 1
        await asyncio.sleep(0.05)

    # Broadcasting to Groups
    for group in groups:
        group_id = group["_id"]
        try:
            await broadcast_msg.copy(chat_id=group_id)
            success_groups += 1
        except (ChatWriteForbidden, PeerIdInvalid):
            failed_groups += 1
        except Exception:
            failed_groups += 1
        await asyncio.sleep(0.05)

    await m.edit(
        f"✅ **Broadcast Completed!**\n\n"
        f"👤 Users:\n   ✅ {success_users} | ❌ {failed_users}\n"
        f"👥 Groups:\n   ✅ {success_groups} | ❌ {failed_groups}"
    )


# ✅ Auto Save Group on Join
@bot.on_chat_member_updated()
async def auto_save_group(_, update):
    member = update.new_chat_member
    if member and member.user and member.user.is_self:
        if member.status == "member":
            await add_group(update.chat.id, update.chat.title or "Unnamed")
        elif member.status in ("kicked", "left"):
            await remove_group(update.chat.id)
