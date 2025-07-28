import importlib
import os

from pyrogram import idle
from revengers import bot

# Path to the modules folder
MODULES_PATH = "revengers/Modules"

# Auto-import all .py files in Modules
for filename in os.listdir(MODULES_PATH):
    if filename.endswith(".py") and not filename.startswith("__"):
        importlib.import_module(f"revengers.Modules.{filename[:-3]}")

if __name__ == "__main__":
    print("[⚔️ REVENGERS BOT STARTED ⚔️]")
    idle()
    print("[❌ BOT STOPPED ❌]")