from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from revengers import bot
from revengers.db import waifu_collection
from pyrogram.enums import ChatType

# /upload command (admin-only, private chat)
@bot.on_message(filters.command("upload") & filters.private)
async def upload_waifu(bot, message: Message):
    if not message.from_user.id in [7576729648]:  # replace OWNER_ID with actual ID
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

# /fdrop command — forced drop in group
@bot.on_message(filters.command("fdrop") & filters.group)
async def fdrop_command(bot, message: Message):
    admins = await bot.get_chat_members(message.chat.id, filter="administrators")
    admin_ids = [admin.user.id for admin in admins]
    if message.from_user.id not in admin_ids:
        return await message.reply("❌ Only admins can use this.")

    waifu = await waifu_collection.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
    if not waifu:
        return await message.reply("⚠️ No waifus in the database.")

    waifu = waifu[0]
    await message.reply_photo(
        photo=waifu["image"],
        caption=f"🎀 Guess this waifu!\n\nReply with /guess <name>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Hint 💡", callback_data="waifu_hint")]
        ])
    )