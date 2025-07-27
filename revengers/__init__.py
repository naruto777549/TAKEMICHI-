from datetime import datetime
start_time = datetime.utcnow()

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "All_in_one",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,  
    parse_mode="HTML"     
)
