"""
Callback Query (Inline tugmalar) uchun handler
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import TEXTS
from keyboards import get_main_menu_keyboard, get_back_to_menu_keyboard, get_social_media_keyboard

logger = logging.getLogger(__name__)

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Inline tugmalar (callback query) uchun handler
    """
    query = update.callback_query
    
    try:
        # Callback query ni acknowledge qilish
        await query.answer()
        
        callback_data = query.data
        user_name = update.effective_user.first_name
        
        logger.info(f"Callback: {callback_data} - User: {user_name} ({update.effective_user.id})")
        
        # Har xil callback data lar uchun javoblar
        if callback_data == 'about':
            await handle_about_callback(query, context)
            
        elif callback_data == 'social':
            await handle_social_callback(query, context)
            
        elif callback_data == 'question':
            await handle_question_callback(query, context)
            
        elif callback_data == 'back_to_menu':
            await handle_back_to_menu_callback(query, context)
            
        else:
            # Noma'lum callback data
            await query.edit_message_text("⚠️ Noma'lum tugma. Qaytadan urinib ko'ring.")
            
    except Exception as e:
        logger.error(f"Callback handler xatolik: {e}")
        try:
            await query.edit_message_text("⚠️ Xatolik yuz berdi. Qaytadan urinib ko'ring.")
        except:
            pass

async def handle_about_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Men haqimda tugmasi bosilganda"""
    reply_markup = get_back_to_menu_keyboard()
    logger.info('about tugmasini bosdi')
    await query.edit_message_text(
        text=TEXTS['about'],
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_social_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Ijtimoiy tarmoqlar tugmasi bosilganda"""
    reply_markup = get_social_media_keyboard()
    
    logger.info('socials tugmasini bosdi')
    
    
    await query.edit_message_text(
        text=TEXTS['social'],
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_question_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Savol yozish tugmasi bosilganda"""
    # User ni savol yozish rejimiga o'tkazish
    context.user_data['waiting_for_question'] = True
    
    logger.info('question tugmasini bosdi')
    
    reply_markup = get_back_to_menu_keyboard()
    
    await query.edit_message_text(
        text=TEXTS['question_prompt'],
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_back_to_menu_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Bosh menyuga qaytish tugmasi bosilganda"""
    # User ma'lumotlarini tozalash
    context.user_data.clear()
    
    reply_markup = get_main_menu_keyboard()
    
    await query.edit_message_text(
        text=TEXTS['welcome'],
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )