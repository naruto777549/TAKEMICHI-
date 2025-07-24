from pyrogram import filters
from pyrogram.types import Message
from datetime import datetime
from revengers import bot
from revengers.db import set_afk, remove_afk, get_afk
import humanize

@bot.on_message(filters.command("afk") & filters.private)
async def set_afk_cmd(client, message: Message):
    reason = message.text.split(None, 1)[1] if len(message.command) > 1 else "No reason"
    await set_afk(message.from_user.id, reason, datetime.utcnow())
    mention = message.from_user.mention
    await message.reply_text(
        f"🚀 {mention}‌ 𝗂𝗌 𝗇𝗈𝗐 𝖠𝖥𝖪! 🚀\n"
        "💤 𝖧𝗆𝗆𝗉𝗁! 𝖫𝖾𝖺𝗏𝖾 𝖺𝗅𝗋𝖾𝖺𝖽𝗒.\𝗇𝖺𝗇𝗀𝗋𝗒 𝖼𝗎𝗍𝖾 𝗉𝗈𝗎𝗍𝗌"
    )

@bot.on_message(filters.text & filters.private)
async def return_from_afk(client, message: Message):
    afk = await get_afk(message.from_user.id)
    if afk:
        duration = datetime.utcnow() - afk["time"]
        readable = humanize.precisedelta(duration)
        await remove_afk(message.from_user.id)
        mention = message.from_user.mention
        await message.reply_text(
            f"🎉 𝖶𝖾𝗅𝖼𝖮𝗆𝖾 𝖻𝖺𝖼𝗄, {mention} !\n"
            "𝖣𝗂𝖽 𝗒𝗈𝗎 𝗋𝗎𝗇 𝗈𝗎𝗍 𝗈𝖿 𝗍𝗂𝗌𝗌𝗎𝖾𝗌, 𝗈𝗋 𝖺𝗋𝖾 𝗒𝗈𝗎 𝗃𝗎𝗌𝗍 𝗁𝖾𝗋𝖾 𝗍𝗈 𝗉𝗋𝖾𝗍𝖾𝗇𝖽 𝗇𝗈𝗍𝗁𝗂𝗇𝗀 𝗁𝖺𝗉𝗉𝖾𝗇𝖾𝖽?\n"
            f"⏱️ 𝖠𝖥𝖪 𝖣𝖴𝖱𝖠𝖳𝖨𝖮𝖭: {readable}"
        )

@bot.on_message(filters.group & filters.text)
async def afk_reply_check(client, message: Message):
    if not message.entities:
        return
    mentioned_ids = [
        ent.user.id for ent in message.entities if ent.type == "mention" and ent.user
    ]
    for uid in mentioned_ids:
        afk = await get_afk(uid)
        if afk:
            duration = datetime.utcnow() - afk["time"]
            readable = humanize.precisedelta(duration)
            mention = f"[{afk.get('first_name', 'User')}](tg://user?id={uid})"
            await message.reply_text(
                f"💤 {mention} 𝗂𝗌 𝖠𝖥𝖪!\n"
                f"⏱️ 𝖠𝖥𝖪 𝗌𝗂𝗇𝖼𝖾: {readable}\n"
                f"✨ {mention} 𝖨𝗌 𝖶𝗂𝗍𝗁 𝖸𝗈𝗎𝗋 𝖲𝗂𝗌"
            )