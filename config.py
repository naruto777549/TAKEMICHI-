import os

API_ID = int(os.getenv("API_ID", "21218274"))
API_HASH = os.getenv("API_HASH", "3474a18b61897c672d315fb330edb213")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7996165975:AAEzC71enTSUrzU7Z7UOJXuc1HnR4hmN-PQ")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot")
ADMINS = list(map(int, os.getenv("ADMINS", "7576729648").split()))
BOT_USER = os.getenv("BOT_USER", "7996165975:AAEzC71enTSUrzU7Z7UOJXuc1HnR4hmN-PQ")
DEVS = list(map(int, os.getenv("DEVS", "7576729648").split()))
LOGS_CHANNEL = int(os.getenv("LOGS_CHANNEL", "-1002623336438"))