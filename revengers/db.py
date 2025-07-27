from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["revengers"]

# Collections
Users = db["users"]
Groups = db["groups"]
users = Users  # alias
Admins = db["admins"]
warns = db["warns"]
chakra_users = db["chakra_users"]
file_collection = db["files"]
waifu_collection = db["waifus"]
afk_collection = db["afk"]
Banned = db["banned"]  # Make sure banned is a collection, not a list

# ----------------- AFK Functions -----------------
async def set_afk(user_id: int, reason: str = "AFK") -> None:
    await afk_collection.update_one(
        {"user_id": user_id},
        {"$set": {"reason": reason, "since": datetime.utcnow()}},
        upsert=True
    )

async def remove_afk(user_id: int) -> None:
    await afk_collection.delete_one({"user_id": user_id})

async def get_afk(user_id: int) -> dict | None:
    return await afk_collection.find_one({"user_id": user_id})

# ----------------- Admin Utilities -----------------
async def add_admin(user_id: int) -> None:
    await Admins.update_one(
        {"_id": user_id},
        {"$set": {"is_admin": True}},
        upsert=True
    )

async def is_admin(user_id: int) -> bool:
    admin = await Admins.find_one({"_id": user_id, "is_admin": True})
    return bool(admin)

async def remove_admin(user_id: int) -> None:
    await Admins.delete_one({"_id": user_id})

# ----------------- Chakra System -----------------
async def get_user_chakra(user_id: int) -> int:
    user = await chakra_users.find_one({"_id": user_id})
    return user.get("chakra", 0) if user else 0

async def add_chakra(user_id: int, amount: int):
    await chakra_users.update_one(
        {"_id": user_id},
        {"$inc": {"chakra": amount}},
        upsert=True
    )

async def can_claim_daily(user_id: int) -> bool:
    user = await chakra_users.find_one({"_id": user_id})
    last = user.get("last_daily") if user else None
    today = datetime.utcnow().date()
    return not last or datetime.strptime(last, "%Y-%m-%d").date() < today

async def claim_daily(user_id: int, amount: int = 100):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    await chakra_users.update_one(
        {"_id": user_id},
        {
            "$set": {"last_daily": today},
            "$inc": {"chakra": amount}
        },
        upsert=True
    )

async def get_top_chakra(limit: int = 10):
    top_users = (
        await chakra_users.find()
        .sort("chakra", -1)
        .limit(limit)
        .to_list(length=limit)
    )
    return top_users

async def remove_chakra(user_id: int, amount: int):
    user = await chakra_users.find_one({"_id": user_id})
    if user:
        current_chakra = user.get("chakra", 0)
        new_chakra = max(current_chakra - amount, 0)
        await chakra_users.update_one(
            {"_id": user_id},
            {"$set": {"chakra": new_chakra}}
        )
    else:
        # Insert with 0 chakra if not found (optional)
        await chakra_users.insert_one({"_id": user_id, "chakra": 0})

# ----------------- Coin Balance System -----------------
async def add_balance(user_id: int, amount: int):
    await chakra_users.update_one(
        {"_id": user_id},
        {"$inc": {"balance": amount}},
        upsert=True
    )

async def reduce_balance(user_id: int, amount: int):
    await chakra_users.update_one(
        {"_id": user_id},
        {"$inc": {"balance": -amount}},
        upsert=True
    )

async def get_balance(user_id: int) -> int:
    user = await chakra_users.find_one({"_id": user_id})
    return user.get("balance", 0) if user else 0

# ----------------- Group Collection Functions -----------------
async def add_group(group_id: int, title: str):
    await Groups.update_one(
        {"_id": group_id},
        {"$set": {"title": title, "joined_at": datetime.utcnow()}},
        upsert=True
    )

async def remove_group(group_id: int):
    await Groups.delete_one({"_id": group_id})

async def is_group_exist(group_id: int) -> bool:
    group = await Groups.find_one({"_id": group_id})
    return bool(group)

async def get_all_groups():
    return [group async for group in Groups.find({})]

# ----------------- Banned Check -----------------
async def is_banned(user_id: int) -> bool:
    banned = await Banned.find_one({"_id": user_id})
    return bool(banned)
