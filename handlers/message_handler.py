"""
Xabarlar uchun handler - Text, Media, Voice
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from config import TEXTS, ADMIN_CHAT_ID, GROUP_CHAT_ID
from keyboards import get_back_to_menu_keyboard
from utils.group_notify import send_question_to_group

logger = logging.getLogger(__name__)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Text xabarlarini qayta ishlash
    """
    try:
        # Agar foydalanuvchi savol yozish rejimida bo'lsa
        if context.user_data.get('waiting_for_question'):
            await handle_user_question(update, context, 'text')
        else:
            await handle_other_messages(update, context)
            
    except Exception as e:
        logger.error(f"Message handler xatolik: {e}")
        await update.message.reply_text("⚠️ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Rasm xabarlarini qayta ishlash"""
    if context.user_data.get('waiting_for_question'):
        await handle_user_question(update, context, 'photo')
    else:
        await update.message.reply_text(TEXTS['menu_command'])

async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Video xabarlarini qayta ishlash"""
    if context.user_data.get('waiting_for_question'):
        await handle_user_question(update, context, 'video')
    else:
        await update.message.reply_text(TEXTS['menu_command'])

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Voice xabarlarini qayta ishlash"""
    if context.user_data.get('waiting_for_question'):
        await handle_user_question(update, context, 'voice')
    else:
        await update.message.reply_text(TEXTS['menu_command'])

async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fayl xabarlarini qayta ishlash"""
    if context.user_data.get('waiting_for_question'):
        await handle_user_question(update, context, 'document')
    else:
        await update.message.reply_text(TEXTS['menu_command'])

async def handle_user_question(update: Update, context: ContextTypes.DEFAULT_TYPE, content_type: str):
    """
    Foydalanuvchi savolini qayta ishlash (barcha tur xabarlar)
    """
    user = update.effective_user
    
    # Content type ga qarab ma'lumot olish
    content_info = get_content_info(update, content_type)
    
    logger.info(f"Savol olindi - User: {user.first_name} ({user.id}), Type: {content_type}")
    
    # Javob yuborish
    response_text = get_response_text(user.first_name, content_type, content_info.get('text', ''))
    
    reply_markup = get_back_to_menu_keyboard()
    
    try:
        await update.message.reply_text(
            text=response_text,
            reply_markup=reply_markup,
            parse_mode='MarkdownV2'  # MarkdownV2 ishlatamiz
        )
    except Exception as e:
        # Agar MarkdownV2 ishlamasa, HTML ishlatamiz
        logger.warning(f"MarkdownV2 xatolik: {e}, HTML ga o'tamiz")
        response_text_html = convert_to_html(response_text)
        await update.message.reply_text(
            text=response_text_html,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    # Savol yozish rejimini tugatish
    context.user_data['waiting_for_question'] = False
    
    # Guruhga xabar yuborish
    if GROUP_CHAT_ID:
        await send_question_to_group(context.bot, user, update.message, content_type, content_info)

def get_content_info(update: Update, content_type: str) -> dict:
    """Xabar turi bo'yicha ma'lumot olish"""
    info = {'text': '', 'file_info': None}
    
    if content_type == 'text':
        info['text'] = update.message.text
        
    elif content_type == 'photo':
        info['text'] = update.message.caption or ''
        info['file_info'] = {
            'file_id': update.message.photo[-1].file_id,
            'file_size': update.message.photo[-1].file_size
        }
        
    elif content_type == 'video':
        info['text'] = update.message.caption or ''
        info['file_info'] = {
            'file_id': update.message.video.file_id,
            'duration': update.message.video.duration,
            'file_size': update.message.video.file_size
        }
        
    elif content_type == 'voice':
        info['file_info'] = {
            'file_id': update.message.voice.file_id,
            'duration': update.message.voice.duration,
            'file_size': update.message.voice.file_size
        }
        
    elif content_type == 'document':
        info['text'] = update.message.caption or ''
        info['file_info'] = {
            'file_id': update.message.document.file_id,
            'file_name': update.message.document.file_name,
            'file_size': update.message.document.file_size
        }
    
    return info

def get_response_text(user_name: str, content_type: str, text_content: str) -> str:
    """Content type ga qarab javob matnini shakllantirish (MarkdownV2 format)"""
    content_names = {
        'text': 'matn xabaringiz',
        'photo': 'rasm xabaringiz',
        'video': 'video xabaringiz', 
        'voice': 'ovozli xabaringiz',
        'document': 'fayl xabaringiz'
    }
    
    content_name = content_names.get(content_type, 'xabaringiz')
    
    # MarkdownV2 uchun maxsus belgilarni escape qilish
    user_name_escaped = escape_markdown(user_name, version=2)
    content_name_escaped = escape_markdown(content_name, version=2)
    
    base_text = f"""

Hurmatli {user_name_escaped}, savolingiz yuborildi\\!
"""
    
    if text_content:
        # Matn satrini escape qilish
        text_escaped = escape_markdown(text_content, version=2)
        base_text += f"""
📝 *Matn:*
_{text_escaped}_
"""
    
    base_text += """
⏰ Tez orada sizga javob beraman\\. 

Boshqa savollaringiz bo'lsa, /start bosing va bemalol yozing\\! 😊
"""
    
    return base_text

def convert_to_html(markdown_text: str) -> str:
    """Markdown matnini HTML ga o'girish"""
    html_text = markdown_text.replace('*', '<b>').replace('*', '</b>')
    html_text = html_text.replace('_', '<i>').replace('_', '</i>')
    html_text = html_text.replace('\\!', '!')
    html_text = html_text.replace('\\.', '.')
    html_text = html_text.replace('\\-', '-')
    
    # HTML formatiga o'girish
    html_text = html_text.replace('✅ <b>Savolingiz qabul qilindi!</b>', '✅ <b>Savolingiz qabul qilindi!</b>')
    html_text = html_text.replace('📝 <b>Matn:</b>', '📝 <b>Matn:</b>')
    
    return html_text

async def handle_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Boshqa xabarlarni qayta ishlash
    """
    await update.message.reply_text(TEXTS['menu_command'])