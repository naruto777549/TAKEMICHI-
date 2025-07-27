import os
import importlib

from revengers import bot
from pyrogram import idle

def load_modules_from_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module_path = f"{directory.replace('/', '.')}.{module_name}"
            try:
                importlib.import_module(module_path)
                print(f"✅ Loaded module: {module_name}")
            except Exception as e:
                print(f"❌ Failed to load {module_name}: {e}")

if __name__ == "__main__":
    load_modules_from_directory("revengers/Modules")
