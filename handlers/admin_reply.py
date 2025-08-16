"""
Admin javob berish handler
Guruhda xabarga reply qilib javob berish
"""

import logging
import re
from telegram import Update
from telegram.ext import ContextTypes

from config import GROUP_CHAT_ID, ADMIN_CHAT_ID

logger = logging.getLogger(__name__)

async def admin_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Guruhda admin reply qilganda foydalanuvchiga javob yuborish
    """
    # Faqat guruhdan kelgan xabarlarni qayta ishlash
    if str(update.effective_chat.id) != GROUP_CHAT_ID:
        return
        
    # Faqat adminlar javob bera oladi
    if str(update.effective_user.id) != ADMIN_CHAT_ID:
        return
        
    # Reply xabari borligini tekshirish
    if not update.message.reply_to_message:
        return
        
    try:
        # Reply qilingan xabardagi User ID ni topish
        replied_message = update.message.reply_to_message
        user_id = extract_user_id_from_message(replied_message.text)
        
        if not user_id:
            await update.message.reply_text("❌ User ID topilmadi. Xabarda User ID bo'lishi kerak.")
            return
            
        # Admin javobini foydalanuvchiga yuborish
        admin_reply = update.message.text
        
        # Foydalanuvchiga javob yuborish
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"""
📬 **Admin javob berdi:**

{admin_reply}

---
💬 Agar yana savolingiz bo'lsa, botda /start bosib yangi savol yuboring.
""",
                parse_mode='Markdown'
            )
            
            # Guruhda tasdiqlash xabari
            await update.message.reply_text(
                f"✅ Javob foydalanuvchiga yuborildi!\n👤 User ID: `{user_id}`",
                parse_mode='Markdown'
            )
            
            logger.info(f"Admin javobi yuborildi - Admin: {update.effective_user.id}, User: {user_id}")
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ Foydalanuvchiga xabar yuborishda xatolik:\n`{str(e)}`",
                parse_mode='Markdown'
            )
            logger.error(f"Admin javobini yuborishda xatolik: {e}")
            
    except Exception as e:
        logger.error(f"Admin reply handler xatolik: {e}")
        await update.message.reply_text("⚠️ Javob yuborishda xatolik yuz berdi.")

def extract_user_id_from_message(message_text: str) -> str:
    """
    Xabar matnidan User ID ni ajratib olish
    """
    if not message_text:
        return None
        
    # User ID pattern: **User ID:** `123456789` yoki **User ID:** 123456789
    patterns = [
        r'\*\*User ID:\*\* `(\d+)`',
        r'\*\*User ID:\*\* (\d+)',
        r'User ID: `(\d+)`',
        r'User ID: (\d+)',
        r'🆔 \*\*User ID:\*\* `(\d+)`',
        r'🆔 \*\*User ID:\*\* (\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message_text)
        if match:
            return match.group(1)
    
    return None