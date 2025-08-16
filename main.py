#!/usr/bin/env python3
"""
Telegram Bot - Asosiy ishga tushirish fayli
Yangilangan versiya: Guruh integratsiyasi va media qo'llab-quvvatlash
"""

import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from config import BOT_TOKEN
from handlers.start_handler import start_command
from handlers.callback_handler import button_callback_handler
from handlers.message_handler import message_handler, photo_handler, video_handler, voice_handler, document_handler
from handlers.admin_reply import admin_reply_handler
from handlers.group_commands import group_info_command, group_help_command

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Botni ishga tushirish funksiyasi"""
    try:
        # Application yaratish
        application = Application.builder().token(BOT_TOKEN).build()
        
        # 🔹 COMMAND HANDLERS - Komandalar
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("info", group_info_command))
        application.add_handler(CommandHandler("help", group_help_command))
        
        # 🔹 CALLBACK HANDLERS - Inline tugmalar
        application.add_handler(CallbackQueryHandler(button_callback_handler))
        
        # 🔹 MEDIA HANDLERS - Rasm, video, ovoz, fayl
        application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
        application.add_handler(MessageHandler(filters.VIDEO, video_handler))
        application.add_handler(MessageHandler(filters.VOICE, voice_handler))
        application.add_handler(MessageHandler(filters.Document.ALL, document_handler))
        
        # 🔹 REPLY HANDLER - Guruhda javob berish (muhim: text dan oldin bo'lishi kerak)
        application.add_handler(MessageHandler(filters.REPLY, admin_reply_handler))
        
        # 🔹 TEXT HANDLER - Matn xabarlar (eng oxirida bo'lishi kerak)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        
        # Botni ishga tushirish
        logger.info("🤖 Bot ishga tushmoqda...")
        logger.info("📱 Guruh integratsiyasi faol")
        logger.info("🎥 Media qo'llab-quvvatlash faol")
        
        print("🎉 Bot muvaffaqiyatli ishga tushdi!")
        print("📋 Qo'llab-quvvatlanadigan formatlar:")
        print("   💬 Text xabarlar")
        print("   🖼️ Rasm + caption")
        print("   🎥 Video + caption") 
        print("   🎤 Ovozli xabar")
        print("   📎 Fayl + caption")
        print("📢 Guruh integratsiyasi: FAOL")
        print("💬 Reply javob berish: FAOL")
        print("📱 To'xtatish uchun Ctrl+C bosing")
        
        # Polling rejimida ishga tushirish
        application.run_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True,
            poll_interval=1.0,
            timeout=10
        )
        
    except KeyboardInterrupt:
        logger.info("👋 Bot to'xtatildi (Ctrl+C)")
        print("\n👋 Bot to'xtatildi!")
        
    except Exception as e:
        logger.error(f"Bot ishga tushishda kritik xatolik: {e}")
        print(f"❌ Kritik xatolik: {e}")
        print("🔧 Tekshiring:")
        print("  • BOT_TOKEN to'g'ri kiritilganmi?")
        print("  • Internet aloqa bormi?")
        print("  • .env fayli mavjudmi?")

if __name__ == '__main__':
    main()