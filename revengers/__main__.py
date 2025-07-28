import importlib
import os
import asyncio

from pyrogram import idle
from revengers import bot

# Path to the modules folder
MODULES_PATH = "revengers/Modules"

# Auto-import all .py files in Modules
for filename in os.listdir(MODULES_PATH):
    if filename.endswith(".py") and not filename.startswith("__"):
        importlib.import_module(f"revengers.Modules.{filename[:-3]}")

async def startup_message():
    try:
        await bot.send_message(
            7576729648,
            "**[⚔️ REVENGERS BOT IS STARTING... ⚔️]**"
        )
    except Exception as e:
        print(f"Failed to send startup message: {e}")

if __name__ == "__main__":
    print("[⚔️ REVENGERS BOT STARTING ⚔️]")
    bot.start()
    asyncio.get_event_loop().run_until_complete(startup_message())
    idle()
    print("[❌ BOT STOPPED ❌]")