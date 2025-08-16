"""
Start komandasi uchun handler
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import TEXTS, GROUP_CHAT_ID
from keyboards import get_main_menu_keyboard
from utils.group_notify import send_new_user_notification

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start komandasi - asosiy menyu ko'rsatadi
    """
    try:
        user_name = update.effective_user.first_name
        logger.info(f"Start komandasi - User: {user_name} ({update.effective_user.id})")
        
        # User ma'lumotlarini tozalash
        context.user_data.clear()
        
        reply_markup = get_main_menu_keyboard()
        
        await update.message.reply_text(
            text=TEXTS['welcome'],
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Yangi foydalanuvchi haqida guruhga xabar yuborish
        if GROUP_CHAT_ID:
            await send_new_user_notification(context.bot, update.effective_user)
        
    except Exception as e:
        logger.error(f"Start komandasi xatolik: {e}")
        await update.message.reply_text("⚠️ Xatolik yuz berdi. Qaytadan urinib ko'ring.")