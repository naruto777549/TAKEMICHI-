from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["revengers"]

# Collections
Users = db["users"]
users = Users  # alias
Admins = db["admins"]
Banned = []  # local cache (if needed)
file_collection = db["files"]
Admins = db["admins"]
waifu_collection = db["waifus"]
afk_collection = db["afk"]

# AFK Functions
async def set_afk(user_id: int, reason: str = "AFK") -> None:
    """Set a user as AFK with a reason and timestamp."""
    await afk_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "reason": reason,
            "since": datetime.utcnow()
        }},
        upsert=True
    )

async def remove_afk(user_id: int) -> None:
    """Remove a user from AFK state."""
    await afk_collection.delete_one({"user_id": user_id})

async def get_afk(user_id: int) -> dict | None:
    """Retrieve AFK data of a user, if any."""
    return await afk_collection.find_one({"user_id": user_id})