"""
Telegram Bot o'rnatish fayli
"""

import os
import shutil
from pathlib import Path

def create_directories():
    """Kerakli papkalarni yaratish"""
    directories = ['handlers', 'utils', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        
        # __init__.py fayllarini yaratish
        if directory in ['handlers', 'utils']:
            init_file = Path(directory) / '__init__.py'
            if not init_file.exists():
                init_file.write_text('"""\n' + f'{directory.title()} moduli\n"""\n')
    
    print("✅ Papkalar yaratildi")

def create_env_file():
    """Agar .env fayli yo'q bo'lsa, .env.example dan nusxalash"""
    if not os.path.exists('.env') and os.path.exists('.env.example'):
        try:
            shutil.copy('.env.example', '.env')
            print("✅ .env fayli yaratildi (.env.example dan)")
            print("⚠️  .env faylida o'z tokeningizni kiriting!")
        except Exception as e:
            print(f"❌ .env faylini yaratishda xatolik: {e}")
    elif os.path.exists('.env'):
        print("✅ .env fayli mavjud")
    else:
        print("⚠️ .env.example fayli topilmadi")

def create_gitignore():
    """Git ignore fayli yaratish"""
    gitignore_content = """# Bot sozlamalari
.env
*.log
bot.log

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    try:
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("✅ .gitignore fayli yaratildi")
    except Exception as e:
        print(f"❌ .gitignore yaratishda xatolik: {e}")

def main():
    """Asosiy o'rnatish funksiyasi"""
    print("🚀 Telegram Bot loyihasi sozlanmoqda...\n")
    
    # Papkalar yaratish
    create_directories()
    
    # .env fayli
    create_env_file()
    
    # .gitignore
    create_gitignore()
    
    print("\n🎉 Loyiha muvaffaqiyatli sozlandi!")
    print("\n📋 Keyingi qadamlar:")
    print("1. .env faylida BOT_TOKEN va ADMIN_CHAT_ID ni to'ldiring")
    print("2. config.py da o'z ma'lumotlaringizni kiriting")
    print("3. requirements.txt dan kutubxonlar o'rnating: pip install -r requirements.txt")
    print("4. Botni ishga tushiring: python main.py")
    
if __name__ == '__main__':
    main()