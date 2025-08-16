# 🤖 Telegram Bot - Python

Telegram bot uchun mukammal strukturali kod. Bot foydalanuvchilar bilan interaktiv muloqot qiladi va admin paneliga ega.

## ✨ Xususiyatlar

- 👤 **Men haqimda** - Shaxsiy ma'lumotlar
- 📱 **Ijtimoiy tarmoqlar** - Barcha ijtimoiy tarmoq linklar
- ❓ **Savol yozish** - Foydalanuvchilar savollar yuborishi
- 🏢 **Guruh integratsiyasi** - Start va savollar guruhga yuboriladi
- 📷 **Media qo'llab-quvvatlash** - Rasm, video, ovoz, fayl qabul qilish
- 💬 **Reply javob berish** - Guruhda reply qilib javob berish
- 🔧 **Admin panel** - Savollarni boshqarish va statistika
- 💾 **Database** - SQLite ma'lumotlar bazasi (ixtiyoriy)
- 📊 **Logging** - Barcha harakatlar log qilinadi

## 📁 Loyiha strukturasi

```
telegram-bot/
├── main.py                 # Asosiy ishga tushirish fayli
├── config.py               # Sozlamalar
├── keyboards.py            # Telegram tugmalari
├── database.py             # Ma'lumotlar bazasi (ixtiyoriy)
├── requirements.txt        # Python kutubxonlari
├── .env.example           # Environment sozlamalari namunasi
├── .env                   # Environment sozlamalari (yaratiladi)
├── setup.py               # Loyihani sozlash
├── run.sh                 # Ishga tushirish skripti
├── handlers/              # Handler funksiyalar
│   ├── __init__.py
│   ├── start_handler.py   # /start komandasi
│   ├── callback_handler.py # Tugma bosilganda
│   ├── message_handler.py # Xabarlar
│   └── admin_commands.py  # Admin komandalar
└── utils/                 # Yordamchi funksiyalar
    ├── __init__.py
    └── admin_notify.py    # Admin xabarlar
```

## 🚀 O'rnatish va sozlash

### 1. Loyihani yuklab oling

```bash
git clone <loyiha-url>
cd telegram-bot
```

### 2. Loyihani sozlang

```bash
python setup.py
```

### 3. Virtual environment yarating

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate     # Windows
```

### 4. Kutubxonlar o'rnating

```bash
pip install -r requirements.txt
```

### 5. Bot yarating

1. Telegram da [@BotFather](https://t.me/botfather) ga boring
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username ini kiriting
4. Tokenni saqlang

### 6. Sozlamalarni to'ldiring

`.env` faylini ochib, o'z ma'lumotlaringizni kiriting:

```env
BOT_TOKEN=1234567890:ABCdefGHijklMNopQRstUVwxyz
ADMIN_CHAT_ID=123456789
```

`config.py` faylida shaxsiy ma'lumotlarni o'zgartiring:

- Ismingiz va kasb ma'lumotlari
- Ijtimoiy tarmoq linklaringiz
- Bot matnlari

### 7. Botni ishga tushiring

```bash
# Oddiy usul
python main.py

# Yoki skript orqali
chmod +x run.sh
./run.sh
```

## 🔧 Konfiguratsiya

### config.py da o'zgartirish kerak bo'lgan qismlar:

```python
# Matnlar
TEXTS = {
    'about': """
👤 **Men haqimda**

Bu yerga o'z ma'lumotlaringizni yozing...
""",
    # ... boshqa matnlar
}

# Ijtimoiy tarmoq linklari
SOCIAL_LINKS = {
    'telegram': 'https://t.me/sizning_username',
    'instagram': 'https://instagram.com/sizning_username',
    'linkedin': 'https://linkedin.com/in/sizning_username',
    'github': 'https://github.com/sizning_username',
    'youtube': 'https://youtube.com/@sizning_kanal'
}
```

## 📋 Qo'shimcha fayllar

```
├── get_group_id.py            # Guruh ID aniqlash
├── handlers/
│   ├── admin_reply.py         # Guruhda reply javob berish
│   └── group_commands.py      # Guruh komandalar
└── utils/
    └── group_notify.py        # Guruhga xabar yuborish
```

## 🎯 Bot qanday ishlaydi?

### 📱 Foydalanuvchi tomonidan:
1. **Start bosish** - Botga `/start` yuboradi
2. **Guruhga xabar** - Yangi user haqida ma'lumot guruhga yuboriladi
3. **Savol yozish** - Text, rasm, video, ovoz, fayl yuborishi mumkin
4. **Guruhga savol** - Barcha savollar guruhga forward qilinadi

### 👨‍💼 Admin tomonidan:
1. **Guruhda savolni ko'rish** - Barcha savollar guruhda ko'rinadi
2. **Reply qilish** - Savolga reply (javob) qilish
3. **Avtomatik yuborish** - Bot javobni foydalanuvchiga yuboradi

### 📷 Qo'llab-quvvatlanadigan formatlar:
- 💬 **Text** - Oddiy matn xabarlar
- 🖼️ **Photo** - Rasm + izoh (caption)
- 🎥 **Video** - Video + izoh
- 🎤 **Voice** - Ovozli xabar
- 📎 **Document** - Har qanday fayl + izoh

Agar `database.py` dan foydalansangiz, quyidagi admin komandalar mavjud:

- `/stats` - Bot statistikasi
- `/questions` - Javob berilmagan savollar
- `/broadcast <xabar>` - Barcha foydalanuvchilarga xabar

Admin komandalarini ishlatish uchun `main.py` ga qo'shing:

```python
from handlers.admin_commands import admin_stats, admin_questions, admin_broadcast

application.add_handler(CommandHandler("stats", admin_stats))
application.add_handler(CommandHandler("questions", admin_questions))
application.add_handler(CommandHandler("broadcast", admin_broadcast))
```

## 🛡️ Xavfsizlik

- `.env` faylini hech qachon Git ga commit qilmang
- Bot tokenini hech kimga bermang
- Admin Chat ID ni to'g'ri kiriting

## 📝 Log fayllar

Barcha bot faolligi `bot.log` faylida saqlanadi:

- Foydalanuvchi harakatlari
- Xatoliklar
- Admin xabarlari

## 🔄 Yangilanishlar

Yangi funksiyalar qo'shish uchun:

1. Yangi handler yarating `handlers/` papkasida
2. `main.py` da ro'yxatdan o'tkazing
3. Kerak bo'lsa `keyboards.py` da tugma qo'shing

## ❓ Tez-tez beriladigan savollar

**Q: Bot ishlamayapti, nima qilishim kerak?**
A: 
1. Bot tokenini tekshiring
2. Internet aloqani tekshiring
3. `bot.log` faylida xatoliklarni ko'ring

**Q: Admin xabarlar kelmayapti?**
A: 
1. `.env` da `ADMIN_CHAT_ID` ni to'g'ri kiritganingizni tekshiring
2. Bot sizga xabar yubora olishini ta'minlang

**Q: Guruhga xabarlar kelmayapti?**
A: 
1. Botni guruhga admin qilib qo'shing
2. GROUP_CHAT_ID to'g'ri kiritganingizni tekshiring
3. `python get_group_id.py` bilan Chat ID ni qayta oling

**Q: Reply qilib javob bermayapti?**
A:
1. Guruhda admin ekanligingizni tekshiring
2. ADMIN_CHAT_ID to'g'ri sozlanganini tekshiring  
3. Xabarda User ID mavjudligini tekshiring

**Q: Qanday media formatlar qo'llab-quvvatlanadi?**
A: Text, Photo, Video, Voice, Document - barchasi qo'llab-quvvatlanadi

## 🤝 Yordam

Savollaringiz bo'lsa, GitHub Issues orqali yozing yoki birTo'g'ridan-to'g'ri bog'laning.

## 📄 Litsenziya

MIT License - bepul foydalanishingiz mumkin.

---

**Bot muvaffaqiyatli ishlashi uchun barcha ko'rsatmalarni bajaring! 🎉**