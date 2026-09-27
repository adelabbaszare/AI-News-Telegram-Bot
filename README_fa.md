# AI-News-Telegram-Bot

![تصویر ربات تلگرام](https://www.webopedia.com/wp-content/uploads/2024/10/what-is-a-telegram-bot-cover-2.webp)
![زبان اصلی](https://img.shields.io/github/languages/top/adelabbaszare/AI-News-Telegram-Bot)
![تعداد زبان‌ها](https://img.shields.io/github/languages/count/adelabbaszare/AI-News-Telegram-Bot)
[![تلگرام](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/learnwithadel)

[🇬🇧 English](README.md) | 🇮🇷 فارسی

رباتی تلگرامی نوشته‌شده با Python که اخبار را دریافت کرده و آن‌ها را در یک کانال یا چت منتشر می‌کند.  
این مخزن شامل نسخه اولیه `news_bot.py` است و برای پیکربندی و اجرا آماده شده است.

---

## 📋 فهرست مطالب

- [قابلیت‌ها](#قابلیت‌ها)
- [ساختار پوشه‌ها و فایل‌ها](#ساختار-پوشه‌ها-و-فایل‌ها)
- [پیش‌نیازها](#پیش‌نیازها)
- [راه‌اندازی](#راه‌اندازی)
- [پیکربندی](#پیکربندی)
- [نحوه استفاده](#نحوه-استفاده)
- [مشارکت](#مشارکت)
- [مجوز](#مجوز)

---

## قابلیت‌ها

- دریافت اخبار از یک منبع مشخص (RSS feed، API یا منبع سفارشی)
- انتشار اخبار در کانال یا چت تلگرام از طریق Bot API
- راه‌اندازی ساده و حداقلی برای استقرار سریع
- آماده برای توسعه بیشتر (موضوعات، زبان‌ها، بازه‌های زمانی و قالب‌بندی)

---

## ساختار پوشه‌ها و فایل‌ها

```bash
AI-News-Telegram-Bot/
│
├─ src/                      # کد ماژولار برنامه
│  ├─ config.py
│  ├─ main.py
│  ├─ models/
│  ├─ services/
│  ├─ repositories/
│  └─ utils/
├─ news_bot_en.py            # اسکریپت قدیمی
├─ news_bot_fa.py            # اسکریپت قدیمی
├─ requirements.txt          # فهرست وابستگی‌ها
├─ send_links.txt            # در زمان اجرا برای ثبت لینک‌های ارسال‌شده ایجاد می‌شود (برای جلوگیری از ارسال اخبار تکراری)
├─ .env                      # متغیرهای پیکربندی
└─ README.md                 # فایل راهنما
```

---

## پیش‌نیازها

- Python **3.13+**
- توکن ربات تلگرام از [@BotFather](https://t.me/BotFather)
- دسترسی به یک منبع خبری: آدرس RSS feed یا News API
- `pip` و یک محیط مجازی برای جداسازی وابستگی‌های پکیج‌ها

---

## راه‌اندازی

1. مخزن را Clone کنید:
```bash
git clone https://github.com/adelabbaszare/AI-News-Telegram-Bot.git
cd AI-News-Telegram-Bot
```

2. (پیشنهاد می‌شود) یک محیط مجازی ایجاد و فعال کنید:
```bash
python -m venv venv
# در Windows:
venv\\Scripts\\activate
# در macOS/Linux:
source venv/bin/activate
```

3. وابستگی‌ها را نصب کنید:
```bash
pip install -r requirements.txt
```

## پیکربندی

لازم است توکن ربات و در صورت نیاز کلید API منبع خبری را تنظیم کنید.

1. یک فایل `.env` در ریشه پروژه ایجاد کنید.

2. متغیرهای نمونه زیر را اضافه کنید:
```env
TELEGRAM_BOT_TOKEN = your_bot_token_here
TELEG­RAM_CHAT_ID = @YourChannel Or ChatID
NEWS_API_KEY = your_api_key_if_any
```

3. در فایل `news_bot.py` مطمئن شوید که مقادیر محیطی/پیکربندی را بارگذاری می‌کنید. برای مثال:
```python
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
NEWS_SOURCE = os.getenv("NEWS_SOURCE_URL")
API_KEY = os.getenv("NEWS_API_KEY")
```

4. سایر تنظیمات موجود در `news_bot.py`، مانند فاصله زمانی دریافت اخبار، تعداد آیتم‌ها در هر پیام و قالب‌بندی پیام را در صورت نیاز تغییر دهید.

## نحوه استفاده

پس از انجام پیکربندی، برنامه را اجرا کنید:
```python
python -m src.main

# اسکریپت‌های قدیمی نیز در طول دوره انتقال همچنان در دسترس هستند
```

ربات اخبار را از منبع مشخص‌شده دریافت، قالب‌بندی و به چت/کانال تلگرام تعیین‌شده ارسال می‌کند.  
برای متوقف کردن آن، کلیدهای `Ctrl + C` را فشار دهید.

## مشارکت

از مشارکت شما استقبال می‌کنیم! مراحل پیشنهادی:

- مخزن را Fork کنید: [![GitHub Forks](https://img.shields.io/github/forks/adelabbaszare/AI-News-Telegram-Bot?style=social)](https://github.com/adelabbaszare/AI-News-Telegram-Bot/fork)
- یک شاخه جدید ایجاد کنید: `git checkout -b feature/your-feature-name`
- تغییرات خود را اعمال کرده و به‌طور کامل تست کنید.
- تغییرات را با یک پیام Commit معنادار ثبت کنید: `e.g: git commit -m "feat: add Persian language support"`
- تغییرات را به Fork خود Push کرده و یک Pull Request ایجاد کنید: [![Pull Requests](https://img.shields.io/github/issues-pr/adelabbaszare/AI-News-Telegram-Bot)](https://github.com/adelabbaszare/AI-News-Telegram-Bot/pulls)
- لطفاً اطمینان حاصل کنید که استاندارد کدنویسی، مدیریت خطا و مستندات پروژه حفظ شوند.

## مجوز

این پروژه متن‌باز و تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر، فایل LICENSE را ببینید.

## تماس / پشتیبانی

اگر با مشکلی مواجه شدید یا پیشنهادی دارید، لطفاً یک Issue در این مخزن ایجاد کنید یا با Adel تماس بگیرید.  
Happy coding 🚀

---

## توسعه

وابستگی‌های توسعه را نصب کنید:

```bash
pip install -r requirements-dev.txt
```

نسخه ماژولار را اجرا کنید:

```bash
python -m src.main
```

تست‌ها را اجرا کنید:

```bash
pytest
```

کیفیت کد را بررسی کنید:

```bash
ruff check .
black --check .
```

این مخزن شامل یک گردش‌کار CI در GitHub Actions است که در زمان Push و Pull Request، ابزارهای Ruff، Black و Pytest را اجرا می‌کند.
