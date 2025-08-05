from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def is_user_admin(bot: Client, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        status = member.status
        logger.info(f"Checking admin status for user {user_id} in chat {chat_id}: Status = {status}")
        
        # Log the enum values for debugging
        logger.info(f"ChatMemberStatus.ADMINISTRATOR = {ChatMemberStatus.ADMINISTRATOR}")
        logger.info(f"ChatMemberStatus.CREATOR = {ChatMemberStatus.CREATOR}")
        
        # Check status using enums
        is_admin = status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
        logger.info(f"Enum check result: User {user_id} is {'admin' if is_admin else 'not admin'}")
        
        # Fallback string check as a precaution
        is_admin_str = status.value in ["administrator", "creator"]
        logger.info(f"String check result: User {user_id} is {'admin' if is_admin_str else 'not admin'}")
        
        # Return True if either check passes
        final_result = is_admin or is_admin_str
        logger.info(f"Final result: User {user_id} is {'admin' if final_result else 'not admin'}")
        return final_result
    except AttributeError as e:
        logger.error(f"AttributeError in is_user_admin for user {user_id} in chat {chat_id}: {str(e)}")
        # Fallback to string comparison if enum fails
        try:
            return member.status.value in ["administrator", "creator"]
        except Exception as e2:
            logger.error(f"Fallback check failed for user {user_id} in chat {chat_id}: {type(e2).__name__}: {str(e2)}")
            return False
    except Exception as e:
        logger.error(f"Error checking admin status for user {user_id} in chat {chat_id}: {type(e).__name__}: {str(e)}")
        return False