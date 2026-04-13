import telebot
import os
import time

# جلب التوكن من البيئة أو من الكود
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    TOKEN = "PUT_YOUR_NEW_TOKEN_HERE"  # 🔴 8581997484:AAGhu3zwL5lmrqhOL2jXKUjXwfBajpT0Qu0

if not TOKEN:
    print("❌ لا يوجد توكن!")
    exit()

# إنشاء البوت
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

print("✅ البوت بدأ التشغيل...")

# أمر start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 البوت شغال 100%\nأهلاً فيك 👋")

# أمر help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "📌 الأوامر:\n/start\n/help")

# رد على أي رسالة
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"📩 رسالتك:\n{message.text}")

# تشغيل مع إعادة محاولة إذا صار خطأ
while True:
    try:
        print("🤖 البوت يعمل...")
        bot.infinity_polling(timeout=30, long_polling_timeout=30)
    except Exception as e:
        print(f"❌ خطأ: {e}")
        print("🔄 إعادة تشغيل خلال 5 ثواني...")
        time.sleep(5)
