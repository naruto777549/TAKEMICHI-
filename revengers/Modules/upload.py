from pyrogram import filters
from pyrogram.types import Message
from revengers import bot
from revengers.db import waifu_collection

OWNER_ID = 7576729648  # Replace with your actual ID

@bot.on_message(filters.command("upload") & filters.private)
async def upload_waifu(bot, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ You aren't authorized to upload waifus.")

    args = message.text.split(maxsplit=3)
    if len(args) < 4:
        return await message.reply("⚠️ Usage: `/upload Name Anime Image_URL`", quote=True)

    _, name, anime, image = args
    caption = f"💘 {name} from *{anime}*"

    await waifu_collection.insert_one({
        "name": name,
        "anime": anime,
        "image": image,
        "caption": caption
    })

    await message.reply_photo(photo=image, caption=f"✅ Added:\n{caption}", quote=True)