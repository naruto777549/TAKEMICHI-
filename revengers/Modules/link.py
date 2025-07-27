from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from config import ADMINS

@bot.on_message(filters.command("link") & filters.private)
async def link_command(bot, message: Message):
    # Check if user is an admin
    if message.from_user.id not in ADMINS:
        return  # silently ignore

    # Check if replying to a message with a file
    if not message.reply_to_message or not (
        message.reply_to_message.video or message.reply_to_message.document
    ):
        return await message.reply("❗ Reply to a video or file with /link to generate a download command.")

    media = message.reply_to_message.video or message.reply_to_message.document
    file_id = media.file_id
    file_name = media.file_name if getattr(media, "file_name", None) else "Unnamed"
    file_size = round(media.file_size / 1024 / 1024, 2)

    text = (
        f"📁 <b>File:</b> <code>{file_name}</code>\n"
        f"📦 <b>Size:</b> {file_size} MB\n"
        f"🔗 <b>Command:</b>\n<code>/get {file_id}</code>"
    )

    await message.reply(text)

from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import get_user_chakra, chakra_users
import re

# Regex for Instagram and YouTube URLs
INSTA_REGEX = r"(https?://)?(www\.)?(instagram\.com|instagr\.am)/[^\s]+"
YT_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/[^\s]+"

@bot.on_message(filters.text)
async def link_handler(bot, message: Message):
    user = message.from_user
    text = message.text

    if re.search(INSTA_REGEX, text) or re.search(YT_REGEX, text):
        user_id = user.id

        chakra = await get_user_chakra(user_id)
        if chakra >= 200:
            await remove_chakra(user_id, 200)
            msg = await message.reply(
                f"✅ **Link Accepted!**\n"
                f"🎥 Downloading video...\n"
                f"💸 200 Chakra points deducted.\n"
                f"💠 Remaining: `{chakra - 200}`"
            )

            try:
                # 📥 Replace this with real video download logic
                video_file = await download_video_from_link(text)

                # 📤 Send the downloaded video
                await message.reply_video(video_file, caption="Here's your video 🔥")
            except Exception as e:
                await msg.edit(f"❌ Failed to download video.\nError: `{e}`")

        else:
            await message.reply(
                f"❌ Not enough Chakra!\n"
                f"🔻 Required: 200\n"
                f"🪙 You Have: `{chakra}`"
            )
    elif text.startswith("http"):
        await message.reply("❌ Only YouTube or Instagram links are supported.")
