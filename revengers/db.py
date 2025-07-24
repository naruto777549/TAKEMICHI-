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

# Admin Utilities
async def add_admin(user_id: int) -> None:
    """Add a user as an admin in the database."""
    await Admins.update_one(
        {"_id": user_id},
        {"$set": {"is_admin": True}},
        upsert=True
    )

async def is_admin(user_id: int) -> bool:
    """Check if a user is an admin."""
    admin = await Admins.find_one({"_id": user_id, "is_admin": True})
    return bool(admin)

async def remove_admin(user_id: int) -> None:
    """Remove a user from admin status."""
    await Admins.delete_one({"_id": user_id})