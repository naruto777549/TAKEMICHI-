from revengers.db import Admins

async def is_admin(user_id: int) -> bool:
    data = await Admins.find_one({"_id": user_id})
    return bool(data)