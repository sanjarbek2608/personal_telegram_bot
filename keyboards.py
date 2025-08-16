"""
Telegram Bot tugmalari va klaviaturalar
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import SOCIAL_LINKS

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
    keyboard = [
        [InlineKeyboardButton("📱 Telegram", url=SOCIAL_LINKS['telegram'])],
        [InlineKeyboardButton("📸 Instagram", url=SOCIAL_LINKS['instagram'])],
        [InlineKeyboardButton("💼 LinkedIn", url=SOCIAL_LINKS['linkedin'])],
        [InlineKeyboardButton("🐙 GitHub", url=SOCIAL_LINKS['github'])],
        [InlineKeyboardButton("📺 YouTube", url=SOCIAL_LINKS['youtube'])],
        [InlineKeyboardButton("🔙 Bosh menyu", callback_data='back_to_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)