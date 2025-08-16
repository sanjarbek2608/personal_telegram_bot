"""
Guruhda ishlatiladigan komandalar
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import GROUP_CHAT_ID, ADMIN_CHAT_ID

logger = logging.getLogger(__name__)

async def group_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /info - Guruh ma'lumotlari
    """
    # Faqat guruhdan ishlaydi
    if str(update.effective_chat.id) != GROUP_CHAT_ID:
        return
        
    # Faqat admin ishlatadi  
    if str(update.effective_user.id) != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ Bu komanda faqat admin uchun!")
        return
        
    try:
        chat_info = f"""
ℹ️ **Guruh ma'lumotlari:**

📊 **Chat ID:** `{update.effective_chat.id}`
📝 **Nom:** {update.effective_chat.title}
👥 **Turi:** {update.effective_chat.type}
🤖 **Bot faol:** ✅

💡 **Qanday ishlaydi:**
• Foydalanuvchilar botda /start bosganida bu guruhga xabar keladi
• Savol yozganlarining xabarlari bu yerda ko'rinadi
• Bu guruhda xabarga reply qilib javob bering
• Javob avtomatik foydalanuvchiga yuboriladi

🔧 **Sozlamalar:**
Bot admin: <@{ADMIN_CHAT_ID}>
Guruh ID: `{GROUP_CHAT_ID}`
"""
        
        await update.message.reply_text(
            text=chat_info,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Group info xatolik: {e}")
        await update.message.reply_text("⚠️ Ma'lumot olishda xatolik yuz berdi.")

async def group_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /help - Guruh yordam
    """
    # Faqat guruhdan ishlaydi
    if str(update.effective_chat.id) != GROUP_CHAT_ID:
        return
        
    help_text = """
🤖 **Bot Guruh Yordam**

📋 **Mavjud komandalar:**
• `/info` - Guruh ma'lumotlari (faqat admin)
• `/help` - Bu yordam matni

💬 **Javob berish:**
1. Foydalanuvchi savolini topish
2. Xabarga reply (javob) qilish
3. Javob matni yozish
4. Yuborish

✅ **Bot avtomatik ravishda:**
• Javobni foydalanuvchiga yuboradi
• Guruhda tasdiqlash xabarini ko'rsatadi

📱 **Qo'llab-quvvatlanadigan formatlar:**
• 💬 Matn xabarlar
• 🖼️ Rasm + caption
• 🎥 Video + caption  
• 🎤 Ovozli xabarlar
• 📎 Fayllar + caption

⚠️ **Eslatma:**
Faqat admin javob bera oladi!
"""
    
    await update.message.reply_text(
        text=help_text,
        parse_mode='Markdown'
    )