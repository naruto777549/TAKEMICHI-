import os

API_ID = int(os.getenv("API_ID", "21218274"))
API_HASH = os.getenv("API_HASH", "3474a18b61897c672d315fb330edb213")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7956858405:AAH_uXebrWLkZagsWsCAeyFLD1EAuNfiVe4")

ADMINS = list(map(int, os.getenv("ADMINS", "7576729648,6642049252").split(",")))