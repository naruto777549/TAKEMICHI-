import os
import importlib

from revengers import bot
from pyrogram import idle

MODULES_PATH = "revengers/Modules"

# Auto-import all .py files from Modules
for filename in os.listdir(MODULES_PATH):
    if filename.endswith(".py") and not filename.startswith("__"):
        importlib.import_module(f"revengers.Modules.{filename[:-3]}")

if __name__ == "__main__":
    bot.start()
    bot.send_message(7576729648, "✅ Bot is Online")
    idle()
    bot.stop()