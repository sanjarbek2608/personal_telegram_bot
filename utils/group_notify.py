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
    first_name = escape_markdown(user.first_name or "Noma'lum", version=2)
    username = f"@{user.username}" if user.username else "mavjud emas"
    full_name = escape_markdown(user.full_name or "Noma'lum", version=2)
    
    # Vaqt formatini alohida o'zgaruvchiga olish
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_time_escaped = escape_markdown(current_time, version=2)
    
    user_info = f"""🆕 *Yangi foydalanuvchi botga start bosdi\\!*

👤 *Ism:* {first_name}
🆔 *User ID:* `{user.id}`
📱 *Username:* {username}
👤 *To'liq ism:* {full_name}
🕐 *Vaqt:* {current_time_escaped}

✨ Yangi a'zo qo'shildi\\!"""
    
    try:
        await bot.send_message(
            chat_id=int(GROUP_CHAT_ID),
            text=user_info,
            parse_mode='MarkdownV2'
        )
        logger.info(f"Yangi foydalanuvchi haqida guruhga xabar yuborildi - User: {user.id}")
        
    except Exception as e:
        logger.error(f"Guruhga yangi foydalanuvchi xabarini yuborishda xatolik: {e}")
        # HTML formatida qayta urinish
        try:
            user_info_html = f"""🆕 <b>Yangi foydalanuvchi botga start bosdi!</b>

👤 <b>Ism:</b> {user.first_name or "Noma'lum"}
🆔 <b>User ID:</b> {user.id}
📱 <b>Username:</b> @{user.username if user.username else "mavjud emas"}
👤 <b>To'liq ism:</b> {user.full_name or "Noma'lum"}
🕐 <b>Vaqt:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✨ Yangi a'zo qo'shildi!"""
            
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
    first_name = escape_markdown(user.first_name or "Noma'lum", version=2)
    username = f"@{user.username}" if user.username else "mavjud emas"
    content_type_title = escape_markdown(content_type.title(), version=2)
    
    # Vaqt formatini alohida o'zgaruvchiga olish
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_time_escaped = escape_markdown(current_time, version=2)
    
    # Asosiy xabar matni
    notification_text = f"""{emoji} *Yangi savol keldi\\!*

👤 *Foydalanuvchi:* {first_name}
🆔 *User ID:* `{user.id}`
📱 *Username:* {username}
📊 *Xabar turi:* {content_type_title}
🕐 *Vaqt:* {current_time_escaped}"""
    
    # Agar matn bo'lsa
    if content_info.get('text'):
        # Matnni to'g'ri escape qilish
        text_content = str(content_info['text'])
        # Maxsus belgilarni escape qilish
        text_escaped = escape_markdown(text_content, version=2)
        notification_text += f"""

📝 *Savol matni:*
{text_escaped}"""
    
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
            file_name = file_info.get('file_name', 'Fayl')
            file_name_escaped = escape_markdown(str(file_name), version=2)
            notification_text += f"\n📎 *Fayl:* {file_name_escaped}"
    
    notification_text += f"""

💬 *Javob berish uchun:* Bu xabarga reply qilib javob yozing"""
    
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
            # HTML format
            html_notification = f"""{emoji} <b>Yangi savol keldi!</b>

👤 <b>Foydalanuvchi:</b> {user.first_name or "Noma'lum"}
🆔 <b>User ID:</b> {user.id}
📱 <b>Username:</b> @{user.username if user.username else "mavjud emas"}
📊 <b>Xabar turi:</b> {content_type.title()}
🕐 <b>Vaqt:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            
            if content_info.get('text'):
                html_notification += f"""

📝 <b>Savol matni:</b>
{content_info['text']}"""
            
            if content_info.get('file_info'):
                file_info = content_info['file_info']
                if content_type == 'photo':
                    html_notification += f"\n🖼️ <b>Rasm yuborildi</b>"
                elif content_type == 'video':
                    duration = file_info.get('duration', 0)
                    html_notification += f"\n🎥 <b>Video:</b> {duration}s davomiyligi"
                elif content_type == 'voice':
                    duration = file_info.get('duration', 0)
                    html_notification += f"\n🎤 <b>Ovozli xabar:</b> {duration}s davomiyligi"
                elif content_type == 'document':
                    file_name = file_info.get('file_name', 'Fayl')
                    html_notification += f"\n📎 <b>Fayl:</b> {file_name}"
            
            html_notification += f"\n\n💬 <b>Javob berish uchun:</b> Bu xabarga reply qilib javob yozing"
            
            sent_message = await bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=html_notification,
                parse_mode='HTML'
            )
            await send_media_to_group(bot, user, content_type, content_info, sent_message.message_id)
        except Exception as e2:
            logger.error(f"HTML formatida ham xatolik: {e2}")

async def send_media_to_group(bot, user, content_type, content_info, reply_to_message_id):
    """Media fayllarni guruhga yuborish"""
    try:
        user_name = user.first_name or "Noma'lum foydalanuvchi"
        
        if content_type == 'photo' and content_info.get('file_info'):
            await bot.send_photo(
                chat_id=GROUP_CHAT_ID,
                photo=content_info['file_info']['file_id'],
                caption=f"👆 {user_name} yuborgan rasm",
                reply_to_message_id=reply_to_message_id
            )
            
        elif content_type == 'video' and content_info.get('file_info'):
            await bot.send_video(
                chat_id=GROUP_CHAT_ID,
                video=content_info['file_info']['file_id'],
                caption=f"👆 {user_name} yuborgan video",
                reply_to_message_id=reply_to_message_id
            )
            
        elif content_type == 'voice' and content_info.get('file_info'):
            await bot.send_voice(
                chat_id=GROUP_CHAT_ID,
                voice=content_info['file_info']['file_id'],
                caption=f"👆 {user_name} yuborgan ovozli xabar",
                reply_to_message_id=reply_to_message_id
            )
            
        elif content_type == 'document' and content_info.get('file_info'):
            await bot.send_document(
                chat_id=GROUP_CHAT_ID,
                document=content_info['file_info']['file_id'],
                caption=f"👆 {user_name} yuborgan fayl",
                reply_to_message_id=reply_to_message_id
            )
    except Exception as e:
        logger.error(f"Media yuborishda xatolik: {e}")

async def send_admin_broadcast_to_group(bot, message):
    """
    Admin xabarini guruhga yuborish
    """
    if not GROUP_CHAT_ID:
        logger.warning("GROUP_CHAT_ID sozlanmagan")
        return
    
    try:
        message_escaped = escape_markdown(str(message), version=2)
        
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

def safe_escape_markdown(text: str) -> str:
    """
    Xavfsiz MarkdownV2 escape qilish
    """
    if not text:
        return ""
    
    # MarkdownV2 da escape qilinishi kerak bo'lgan belgilar
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    result = str(text)
    for char in special_chars:
        result = result.replace(char, f'\\{char}')
    
    return result