import os
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# Bot sozlamalari
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')  # Shaxsiy admin chat
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')  # Guruh chat ID

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylda topilmadi!")

if not ADMIN_CHAT_ID:
    print("⚠️ ADMIN_CHAT_ID sozlanmagan. Admin xabarlar yuborilmaydi.")

if not GROUP_CHAT_ID:
    print("⚠️ GROUP_CHAT_ID sozlanmagan. Guruh xabarlari yuborilmaydi.")

# Matnlar
TEXTS = {
    'welcome': """
👋 Assalomu alaykum! Botga xush kelibsiz!
Quyidagi tugmalardan birini tanlang:
""",
    
    'about': """
👤 **Men haqimda**

Salom! Men [Ismingiz] - Python dasturchi va Telegram bot yaratuvchisiman.

🎯 **Faoliyatim:**
• Python dasturlash
• Telegram bot yaratish  
• Web development
• Ma'lumotlar tahlili

📚 **Ko'nikmalarim:**
• Python, Django, Flask
• Telegram Bot API
• PostgreSQL, MongoDB  
• Git, Docker

🏆 **Maqsadlarim:**
Zamonaviy texnologiyalar yordamida foydali botlar va dasturlar yaratish
""",
    
    'social': """
📱 **Ijtimoiy tarmoqlarimda kuzatib boring:**

Quyidagi linklar orqali men bilan bog'laning:
""",
    
    'question_prompt': """
❓ **Savol yozish**

Menga savolingizni yozing! 

📝 Quyidagi mavzular bo'yicha yordam bera olaman:
• Python dasturlash
• Telegram bot yaratish
• Web development  
• Texnik masalalar
• Boshqa IT mavzular

Savolingizni yozing, tez orada javob beraman! 👇
""",
    
    'question_received': """
✅ **Savolingiz qabul qilindi!**

Hurmatli {user_name}, savolingiz uchun rahmat!

📝 **Sizning savolingiz:**
_{question}_

⏰ Tez orada sizga javob beriladi. 
📬 Javob ushbu botda yoki shaxsiy xabar orqali yuboriladi.

Boshqa savollaringiz bo'lsa, bemalol yozing! 😊
""",

    'menu_command': """
🤖 Menyu uchun /start buyrug'ini yuboring!
"""
}

# Ijtimoiy tarmoq linklari
SOCIAL_LINKS = {
    'telegram': os.getenv("TELEGRAM"),
    'instagram': os.getenv("INSTAGRAM"), 
    'linkedin': os.getenv("LINKEDIN"),
    'github': os.getenv("GITHUB"),   # agar .env da GITHUB bo‘lsa
    'youtube': os.getenv("YOUTUBE"), # agar .env da YOUTUBE bo‘lsa
    'facebook': os.getenv("FACEBOOK"),
    'x': os.getenv("X"),
}