from pyrogram.filters import Filter
from pyrogram.types import Message
from revengers.db import Admins

class IsAdmin(Filter):
    async def __call__(self, _, __, message: Message):
        user_id = message.from_user.id
        admin = await Admins.find_one({"_id": user_id})
        return admin is not None and admin.get("is_admin", False)

is_admin = IsAdmin()