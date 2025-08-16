#!/bin/bash

# Telegram Bot ishga tushirish skripti

echo "🤖 Telegram Bot ishga tushmoqda..."

# Virtual environment tekshirish
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment yaratilmoqda..."
    python3 -m venv venv
fi

# Virtual environment faollashtirish
echo "🔄 Virtual environment faollashtirilmoqda..."
source venv/bin/activate

# Kerakli kutubxonalarni o'rnatish
echo "📚 Kutubxonlar o'rnatilmoqda..."
pip install -r requirements.txt

# .env fayl tekshirish
if [ ! -f ".env" ]; then
    echo "⚠️  .env fayli topilmadi!"
    echo "📝 .env.example faylini .env ga nusxalab, sozlamalarni to'ldiring"
    exit 1
fi

# Botni ishga tushirish
echo "🚀 Bot ishga tushirilmoqda..."
python main.py