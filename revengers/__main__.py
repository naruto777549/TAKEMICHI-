import asyncio
import importlib
import os
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Bot setup
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Module loading function
async def load_modules():
    modules_path = "revengers/Modules"
    for filename in os.listdir(modules_path):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            try:
                importlib.import_module(f"revengers.Modules.{module_name}")
                print(f"✅ Loaded module: {module_name}")
            except Exception as e:
                print(f"❌ Failed to load module: {module_name} | Error: {e}")

# Main bot loop
async def main():
    await load_modules()
    print("🚀 All modules loaded. Starting bot...")
    await app.start()
    print("🤖 BOT IS READY!")
    await idle()
    await app.stop()
    print("👋 BOT STOPPED.")

# To keep the bot alive
from pyrogram import idle

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
