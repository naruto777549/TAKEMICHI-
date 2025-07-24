from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["revengers"]

Users = db["users"]
users = Users
Banned = []  
file_collection = db["files"]

Admins = db["admins"]  
waifu_collection = db["waifus"]

afk_collection = db["afk"]  

async def set_afk(user_id: int, reason: str = "AFK"):
    await afk_collection.update_one(
        {"user_id": user_id},
        {"$set": {"reason": reason, "since": datetime.utcnow()}},
        upsert=True
    )

async def remove_afk(user_id: int):
    await afk_collection.delete_one({"user_id": user_id})

async def get_afk(user_id: int):
    return await afk_collection.find_one({"user_id": user_id})