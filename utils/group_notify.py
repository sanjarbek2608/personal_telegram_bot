"""
Guruhga xabar yuborish funksiyalari
"""

import logging
from datetime import datetime
from config import GROUP_CHAT_ID

logger = logging.getLogger(__name__)

async def send_new_user_notification(bot, user):
    """
    Yangi foydalanuvchi start bosganda guruhga xabar yuborish
    """
    if not GROUP_CHAT_ID:
        logger.warning("GROUP_CHAT_ID sozlanmagan, guruh xabari yuborilmaydi")
        return
    
    user_info = f"""
🆕 **Yangi foydalanuvchi botga start bosdi!**

👤 **Ism:** {user.first_name}
🆔 **User ID:** `{user.id}`
📱 **Username:** @{user.username or 'mavjud emas'}
👤 **To'liq ism:** {user.full_name}
🕐 **Vaqt:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✨ Yangi a'zo qo'shildi!
"""
    
    try:
        await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=user_info,
            parse_mode='Markdown'
        )
        logger.info(f"Yangi foydalanuvchi haqida guruhga xabar yuborildi - User: {user.id}")
        
    except Exception as e:
        logger.error(f"Guruhga yangi foydalanuvchi xabarini yuborishda xatolik: {e}")

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
    
    # Asosiy xabar matni
    notification_text = f"""
{emoji} **Yangi savol keldi!**

👤 **Foydalanuvchi:** {user.first_name}
🆔 **User ID:** `{user.id}`
📱 **Username:** @{user.username or 'mavjud emas'}
📊 **Xabar turi:** {content_type.title()}
🕐 **Vaqt:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Agar matn bo'lsa
    if content_info.get('text'):
        notification_text += f"""
📝 **Savol matni:**
_{content_info['text']}_
"""
    
    # Fayl ma'lumotlari
    if content_info.get('file_info'):
        file_info = content_info['file_info']
        
        if content_type == 'photo':
            notification_text += f"\n🖼️ **Rasm yuborildi**"
            
        elif content_type == 'video':
            duration = file_info.get('duration', 0)
            notification_text += f"\n🎥 **Video:** {duration}s davomiyligi"
            
        elif content_type == 'voice':
            duration = file_info.get('duration', 0)
            notification_text += f"\n🎤 **Ovozli xabar:** {duration}s davomiyligi"
            
        elif content_type == 'document':
            file_name = file_info.get('file_name', 'Fayl')
            notification_text += f"\n📎 **Fayl:** {file_name}"
    
    notification_text += f"""

💬 **Javob berish uchun:** Bu xabarga reply qilib javob yozing
"""
    
    try:
        # Avval matn xabarni yuborish
        sent_message = await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=notification_text,
            parse_mode='Markdown'
        )
        
        # Agar media bo'lsa, uni ham yuborish
        if content_type == 'photo' and content_info.get('file_info'):
            await bot.send_photo(
                chat_id=GROUP_CHAT_ID,
                photo=content_info['file_info']['file_id'],
                caption=f"👆 {user.first_name} yuborgan rasm",
                reply_to_message_id=sent_message.message_id
            )
            
        elif content_type == 'video' and content_info.get('file_info'):
            await bot.send_video(
                chat_id=GROUP_CHAT_ID,
                video=content_info['file_info']['file_id'],
                caption=f"👆 {user.first_name} yuborgan video",
                reply_to_message_id=sent_message.message_id
            )
            
        elif content_type == 'voice' and content_info.get('file_info'):
            await bot.send_voice(
                chat_id=GROUP_CHAT_ID,
                voice=content_info['file_info']['file_id'],
                caption=f"👆 {user.first_name} yuborgan ovozli xabar",
                reply_to_message_id=sent_message.message_id
            )
            
        elif content_type == 'document' and content_info.get('file_info'):
            await bot.send_document(
                chat_id=GROUP_CHAT_ID,
                document=content_info['file_info']['file_id'],
                caption=f"👆 {user.first_name} yuborgan fayl",
                reply_to_message_id=sent_message.message_id
            )
        
        logger.info(f"Guruhga savol xabari yuborildi - User: {user.id}, Type: {content_type}")
        
    except Exception as e:
        logger.error(f"Guruhga savol xabarini yuborishda xatolik: {e}")

async def send_admin_broadcast_to_group(bot, message):
    """
    Admin xabarini guruhga yuborish
    """
    if not GROUP_CHAT_ID:
        logger.warning("GROUP_CHAT_ID sozlanmagan")
        return
        
    try:
        await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f"📢 **Admin e'loni:**\n\n{message}",
            parse_mode='Markdown'
        )
        logger.info("Admin e'loni guruhga yuborildi")
        
    except Exception as e:
        logger.error(f"Guruhga admin e'lonini yuborishda xatolik: {e}")