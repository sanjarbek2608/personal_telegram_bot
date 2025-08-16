#!/usr/bin/env python3
"""
Guruh Chat ID aniqlash uchun yordamchi skript
"""

import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv('BOT_TOKEN')

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chat ID ni aniqlash"""
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    chat_title = update.effective_chat.title or "Shaxsiy chat"
    
    message = f"""
🆔 **Chat Ma'lumotlari:**

📊 **Chat ID:** `{chat_id}`
📝 **Nom:** {chat_title}
👥 **Turi:** {chat_type}

💡 **Ko'rsatma:**
Agar bu guruh uchun bot yaratmoqchi bo'lsangiz:
1. Yuqoridagi Chat ID ni nusxalang
2. .env faylida GROUP_CHAT_ID= ga qo'ying
3. Botni qayta ishga tushiring

Masalan: GROUP_CHAT_ID={chat_id}
"""
    
    await update.message.reply_text(
        text=message,
        parse_mode='Markdown'
    )
    
    print(f"Chat ID topildi: {chat_id} ({chat_type} - {chat_title})")

def main():
    """Chat ID aniqlash botini ishga tushirish"""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN topilmadi! .env faylni tekshiring.")
        return
    
    print("🔍 Chat ID aniqlash boti ishlamoqda...")
    print("📱 Botni guruhga qo'shing va istalgan xabar yuboring")
    print("🆔 Chat ID ni olasiz")
    print("⏹️ To'xtatish uchun Ctrl+C bosing\n")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Barcha xabarlarga javob berish
    application.add_handler(MessageHandler(filters.ALL, get_chat_id))
    
    # Botni ishga tushirish
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Chat ID bot to'xtatildi!")