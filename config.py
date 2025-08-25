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

Assalomu aleykum! 
**Mening ismim: Sanjarbek Xayrulloyev!**
**Navoiy viloyati, Qiziltepa tumanida tug'ilganman.**
**Qolgan ma'lumotlar to'ldirilmoqda 🙂**
""",
    
    'social': """
📱 **Ijtimoiy tarmoqlardagi sahifalarim:**

Quyidagi linklarni bosish orqali sahifalarga o'tishingiz mumkin:
""",
    
    'question_prompt': """
❓ **Savol yozish**

Menga savolingizni yozing, tez orada javob beraman! 👇
""",
    
    'question_received': """
✅ **Savolingiz qabul qilindi!**

Hurmatli {user_name}, savolingiz uchun rahmat!

📝 **Sizning savolingiz:**
_{question}_

⏰ Tez orada sizga javob beraman. 

Boshqa savollaringiz bo'lsa, /start ni bosing va bemalol yozing! 😊
""",

    'menu_command': """
🤖 Menyu uchun /start buyrug'ini yuboring!
"""
}

# Ijtimoiy tarmoq linklari
SOCIAL_LINKS = {
    'instagram': os.getenv("INSTAGRAM"), 
    'linkedin': os.getenv("LINKEDIN"),
    'facebook': os.getenv("FACEBOOK"),
    'x': os.getenv("X"),
    'telegram': os.getenv("TELEGRAM"),
}