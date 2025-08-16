"""
Guruhga xabar yuborish funksiyalari
"""

import logging
from datetime import datetime
from telegram.helpers import escape_markdown
from config import GROUP_CHAT_ID

logger = logging.getLogger(__name__)

async def send_new_user_notification(bot, user):
    """
    Yangi foydalanuvchi start bosganda guruhga xabar yuborish
    """
    if not GROUP_CHAT_ID:
        logger.warning("GROUP_CHAT_ID sozlanmagan, guruh xabari yuborilmaydi")
        return
    
    # Ma'lumotlarni escape qilish
    first_name = escape_markdown(user.first_name, version=2)
    username = f"@{user.username}" if user.username else "mavjud emas"
    full_name = escape_markdown(user.full_name, version=2)
    
    # Vaqt formatini alohida o'zgaruvchiga olish
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_time_escaped = escape_markdown(current_time, version=2)
    
    user_info = f"""
🆕 *Yangi foydalanuvchi botga start bosdi\\!*

👤 *Ism:* {first_name}
🆔 *User ID:* `{user.id}`
📱 *Username:* {username}
👤 *To'liq ism:* {full_name}
🕐 *Vaqt:* {current_time_escaped}

✨ Yangi a'zo qo'shildi\\!
"""
    
    try:
        await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=user_info,
            parse_mode='MarkdownV2'
        )
        logger.info(f"Yangi foydalanuvchi haqida guruhga xabar yuborildi - User: {user.id}")
        
    except Exception as e:
        logger.error(f"Guruhga yangi foydalanuvchi xabarini yuborishda xatolik: {e}")
        # HTML formatida qayta urinish
        try:
            user_info_html = convert_markdown_to_html(user_info)
            await bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=user_info_html,
                parse_mode='HTML'
            )
        except Exception as e2:
            logger.error(f"HTML formatida ham xatolik: {e2}")

async def send_question_to_group(bot, user, message, content_type, content_info):
    """
    Foydalanuvchi savoli haqida guruhga xabar yuborish
    """
    if not GROUP_CHAT_ID:
        logger.warning("GROUP_CHAT_ID sozlanmagan, guruh xabari yuborilmaydi")
        return
    
    # Xabar turi bo'yicha emoji
    type_emojis = {
        'text': '💬',
        'photo': '🖼️',
        'video': '🎥',
        'voice': '🎤', 
        'document': '📎'
    }
    
    emoji = type_emojis.get(content_type, '📝')
    
    # Ma'lumotlarni escape qilish
    first_name = escape_markdown(user.first_name, version=2)
    username = f"@{user.username}" if user.username else "mavjud emas"
    content_type_title = escape_markdown(content_type.title(), version=2)
    
    # Vaqt formatini alohida o'zgaruvchiga olish
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_time_escaped = escape_markdown(current_time, version=2)
    
    # Asosiy xabar matni
    notification_text = f"""
{emoji} *Yangi savol keldi\\!*

👤 *Foydalanuvchi:* {first_name}
🆔 *User ID:* `{user.id}`
📱 *Username:* {username}
📊 *Xabar turi:* {content_type_title}
🕐 *Vaqt:* {current_time_escaped}
"""
    
    # Agar matn bo'lsa
    if content_info.get('text'):
        text_escaped = escape_markdown(content_info['text'], version=2)
        notification_text += f"""
📝 *Savol matni:*
_{text_escaped}_
"""
    
    # Fayl ma'lumotlari
    if content_info.get('file_info'):
        file_info = content_info['file_info']
        
        if content_type == 'photo':
            notification_text += f"\n🖼️ *Rasm yuborildi*"
            
        elif content_type == 'video':
            duration = file_info.get('duration', 0)
            notification_text += f"\n🎥 *Video:* {duration}s davomiyligi"
            
        elif content_type == 'voice':
            duration = file_info.get('duration', 0)
            notification_text += f"\n🎤 *Ovozli xabar:* {duration}s davomiyligi"
            
        elif content_type == 'document':
            file_name = escape_markdown(file_info.get('file_name', 'Fayl'), version=2)
            notification_text += f"\n📎 *Fayl:* {file_name}"
    
    notification_text += f"""

💬 *Javob berish uchun:* Bu xabarga reply qilib javob yozing
"""
    
    try:
        # Avval matn xabarni yuborish
        sent_message = await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=notification_text,
            parse_mode='MarkdownV2'
        )
        
        # Agar media bo'lsa, uni ham yuborish
        await send_media_to_group(bot, user, content_type, content_info, sent_message.message_id)
        
        logger.info(f"Guruhga savol xabari yuborildi - User: {user.id}, Type: {content_type}")
        
    except Exception as e:
        logger.error(f"Guruhga savol xabarini yuborishda xatolik: {e}")
        # HTML formatida qayta urinish
        try:
            notification_text_html = convert_markdown_to_html(notification_text)
            sent_message = await bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=notification_text_html,
                parse_mode='HTML'
            )
            await send_media_to_group(bot, user, content_type, content_info, sent_message.message_id)
        except Exception as e2:
            logger.error(f"HTML formatida ham xatolik: {e2}")

async def send_media_to_group(bot, user, content_type, content_info, reply_to_message_id):
    """Media fayllarni guruhga yuborish"""
    try:
        if content_type == 'photo' and content_info.get('file_info'):
            await bot.send_photo(
                chat_id=GROUP_CHAT_ID,
                photo=content_info['file_info']['file_id'],
                caption=f"👆 {user.first_name} yuborgan rasm",
                reply_to_message_id=reply_to_message_id
            )
            
        elif content_type == 'video' and content_info.get('file_info'):
            await bot.send_video(
                chat_id=GROUP_CHAT_ID,
                video=content_info['file_info']['file_id'],
                caption=f"👆 {user.first_name} yuborgan video",
                reply_to_message_id=reply_to_message_id
            )
            
        elif content_type == 'voice' and content_info.get('file_info'):
            await bot.send_voice(
                chat_id=GROUP_CHAT_ID,
                voice=content_info['file_info']['file_id'],
                caption=f"👆 {user.first_name} yuborgan ovozli xabar",
                reply_to_message_id=reply_to_message_id
            )
            
        elif content_type == 'document' and content_info.get('file_info'):
            await bot.send_document(
                chat_id=GROUP_CHAT_ID,
                document=content_info['file_info']['file_id'],
                caption=f"👆 {user.first_name} yuborgan fayl",
                reply_to_message_id=reply_to_message_id
            )
    except Exception as e:
        logger.error(f"Media yuborishda xatolik: {e}")

def convert_markdown_to_html(markdown_text: str) -> str:
    """MarkdownV2 ni HTML ga o'girish"""
    html_text = markdown_text
    
    # Escape qilingan belgilarni tiklash
    html_text = html_text.replace('\\!', '!')
    html_text = html_text.replace('\\.', '.')
    html_text = html_text.replace('\\-', '-')
    html_text = html_text.replace('\\(', '(')
    html_text = html_text.replace('\\)', ')')
    
    # Markdown formatlarni HTML ga o'girish
    html_text = html_text.replace('*', '<b>').replace('*', '</b>')
    html_text = html_text.replace('_', '<i>').replace('_', '</i>')
    html_text = html_text.replace('`', '<code>').replace('`', '</code>')
    
    return html_text

async def send_admin_broadcast_to_group(bot, message):
    """
    Admin xabarini guruhga yuborish
    """
    if not GROUP_CHAT_ID:
        logger.warning("GROUP_CHAT_ID sozlanmagan")
        return
    
    message_escaped = escape_markdown(message, version=2)
    
    try:
        await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f"📢 *Admin e'loni:*\n\n{message_escaped}",
            parse_mode='MarkdownV2'
        )
        logger.info("Admin e'loni guruhga yuborildi")
        
    except Exception as e:
        logger.error(f"Guruhga admin e'lonini yuborishda xatolik: {e}")
        # HTML formatida qayta urinish
        try:
            await bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=f"📢 <b>Admin e'loni:</b>\n\n{message}",
                parse_mode='HTML'
            )
        except Exception as e2:
            logger.error(f"HTML formatida ham xatolik: {e2}")