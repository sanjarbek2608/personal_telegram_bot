# """
# Admin komandalar (ixtiyoriy)
# """

# import logging
# from telegram import Update
# from telegram.ext import ContextTypes

# from config import ADMIN_CHAT_ID
# from database import db

# logger = logging.getLogger(__name__)

# async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """
#     Admin uchun statistika ko'rsatish
#     Faqat admin foydalana oladi
#     """
#     # Admin tekshirish
#     if str(update.effective_user.id) != ADMIN_CHAT_ID:
#         await update.message.reply_text("❌ Bu komanda faqat admin uchun!")
#         return
    
#     try:
#         stats = db.get_user_stats()
        
#         stats_text = f"""
# 📊 **Bot Statistikasi**

# 👥 **Jami foydalanuvchilar:** {stats['total_users']}
# ❓ **Jami savollar:** {stats['total_questions']}  
# ⏳ **Javob kutayotgan:** {stats['unanswered_questions']}
# ✅ **Javob berilgan:** {stats['total_questions'] - stats['unanswered_questions']}

# 📈 **Faollik:**
# Bugungi yangi foydalanuvchilar va savollar statistikasi
#         """
        
#         await update.message.reply_text(
#             text=stats_text,
#             parse_mode='Markdown'
#         )
        
#     except Exception as e:
#         logger.error(f"Admin stats xatolik: {e}")
#         await update.message.reply_text("⚠️ Statistika olishda xatolik yuz berdi.")

# async def admin_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """
#     Javob berilmagan savollarni ko'rsatish
#     """
#     # Admin tekshirish
#     if str(update.effective_user.id) != ADMIN_CHAT_ID:
#         await update.message.reply_text("❌ Bu komanda faqat admin uchun!")
#         return
    
#     try:
#         questions = db.get_unanswered_questions()
        
#         if not questions:
#             await update.message.reply_text("✅ Barcha savollarga javob berilgan!")
#             return
        
#         response = "❓ **Javob kutayotgan savollar:**\n\n"
        
#         for q in questions[:5]:  # Faqat 5 ta savolni ko'rsatish
#             username = f"@{q['username']}" if q['username'] else "username yo'q"
#             response += f"""
# **#{q['id']}** - {q['first_name']} ({username})
# 📝 _{q['question']}_
# ⏰ {q['created_at']}

# """
        
#         if len(questions) > 5:
#             response += f"\n... va yana {len(questions) - 5} ta savol"
        
#         await update.message.reply_text(
#             text=response,
#             parse_mode='Markdown'
#         )
        
#     except Exception as e:
#         logger.error(f"Admin questions xatolik: {e}")
#         await update.message.reply_text("⚠️ Savollarni olishda xatolik yuz berdi.")

# async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """
#     Barcha foydalanuvchilarga xabar yuborish
#     Foydalanish: /broadcast <xabar>
#     """
#     # Admin tekshirish
#     if str(update.effective_user.id) != ADMIN_CHAT_ID:
#         await update.message.reply_text("❌ Bu komanda faqat admin uchun!")
#         return
    
#     # Xabar matnini olish
#     if not context.args:
#         await update.message.reply_text(
#             "📢 Foydalanish: `/broadcast xabar matni`",
#             parse_mode='Markdown'
#         )
#         return
    
#     message_text = ' '.join(context.args)
    
#     try:
#         # Barcha foydalanuvchilarni olish
#         with sqlite3.connect(db.db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute('SELECT user_id FROM users')
#             users = cursor.fetchall()
        
#         success_count = 0
#         failed_count = 0
        
#         # Har bir foydalanuvchiga xabar yuborish
#         for user_tuple in users:
#             user_id = user_tuple[0]
#             try:
#                 await context.bot.send_message(
#                     chat_id=user_id,
#                     text=f"📢 **Admin xabari:**\n\n{message_text}",
#                     parse_mode='Markdown'
#                 )
#                 success_count += 1
                
#             except Exception as e:
#                 logger.warning(f"User {user_id} ga xabar yuborib bo'lmadi: {e}")
#                 failed_count += 1
        
#         result_text = f"""
# ✅ **Broadcast tugadi**

# 📤 **Yuborildi:** {success_count}
# ❌ **Xatolik:** {failed_count}
# 👥 **Jami:** {len(users)}
#         """
        
#         await update.message.reply_text(
#             text=result_text,
#             parse_mode='Markdown'
#         )
        
#     except Exception as e:
#         logger.error(f"Broadcast xatolik: {e}")
#         await update.message.reply_text("⚠️ Broadcast yuborishda xatolik yuz berdi.")