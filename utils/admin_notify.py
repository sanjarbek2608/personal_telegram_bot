"""
Admin ga xabar yuborish funksiyalari
"""

import logging
from config import ADMIN_CHAT_ID

logger = logging.getLogger(__name__)

async def send_question_to_admin(bot, user, question):
    """
    Admin ga yangi savol haqida xabar yuborish
    """
    if not ADMIN_CHAT_ID:
        logger.warning("ADMIN_CHAT_ID sozlanmagan, admin xabari yuborilmaydi")
        return
    
    admin_message = f"""
🆕 **Yangi savol keldi!**

👤 **Foydalanuvchi:** {user.first_name}
🆔 **User ID:** {user.id}
📱 **Username:** @{user.username or 'mavjud emas'}

📝 **Savol:**
{question}

⏰ **Vaqt:** {user.id} (Unix timestamp)
"""
    
    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message,
            parse_mode='Markdown'
        )
        logger.info(f"Admin ga xabar yuborildi - User: {user.id}")
        
    except Exception as e:
        logger.error(f"Admin ga xabar yuborishda xatolik: {e}")

async def send_admin_message(bot, message):
    """
    Admin ga umumiy xabar yuborish
    """
    if not ADMIN_CHAT_ID:
        logger.warning("ADMIN_CHAT_ID sozlanmagan")
        return
        
    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        logger.info("Admin ga xabar yuborildi")
        
    except Exception as e:
        logger.error(f"Admin ga xabar yuborishda xatolik: {e}")