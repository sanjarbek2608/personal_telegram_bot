"""
Telegram Bot tugmalari va klaviaturalar
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    """Asosiy menyu tugmalari"""
    keyboard = [
        [InlineKeyboardButton("👤 Men haqimda", callback_data='about')],
        [InlineKeyboardButton("📱 Ijtimoiy tarmoqlar", callback_data='social')],
        [InlineKeyboardButton("❓ Savol yozish", callback_data='question')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_menu_keyboard():
    """Asosiy menyuga qaytish tugmasi"""
    keyboard = [[InlineKeyboardButton("🔙 Bosh menyu", callback_data='back_to_menu')]]
    return InlineKeyboardMarkup(keyboard)

def get_social_media_keyboard():
    """Ijtimoiy tarmoqlar tugmalari"""
    # SOCIAL_LINKS ni bu yerda import qilish circular import dan saqlanish uchun
    from config import SOCIAL_LINKS
    
    keyboard = []
    
    # Har bir ijtimoiy tarmoq uchun tugma yaratish (faqat link mavjud bo'lsa)
    social_buttons = [
        ("📸 Instagram", SOCIAL_LINKS.get('instagram')),
        ("💼 LinkedIn", SOCIAL_LINKS.get('linkedin')),
        ("📘 Facebook", SOCIAL_LINKS.get('facebook')),
        ("📘 X (Twitter)", SOCIAL_LINKS.get('x')),
        ("📱 Telegram", SOCIAL_LINKS.get('telegram'))
    ]
    
    # Faqat link mavjud bo'lgan tugmalarni qo'shish
    for button_text, link in social_buttons:
        if link and link.strip():  # Link mavjud va bo'sh emas
            keyboard.append([InlineKeyboardButton(button_text, url=link)])
    
    # Agar hech qanday ijtimoiy tarmoq linki yo'q bo'lsa
    if not keyboard:
        keyboard.append([InlineKeyboardButton("⚠️ Linklar sozlanmagan", callback_data='no_links')])
    
    # Har doim bosh menyuga qaytish tugmasini qo'shish
    keyboard.append([InlineKeyboardButton("🔙 Bosh menyu", callback_data='back_to_menu')])
    
    return InlineKeyboardMarkup(keyboard)