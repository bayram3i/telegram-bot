import telebot
import os

# ياخذ التوكن من Render أو من الكود
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    TOKEN = "PUT_YOUR_TOKEN_HERE"  # ←8581997484:AAGhu3zwL5lmrqhOL2jXKUjXwfBajpT0Qu0

if not TOKEN:
    print("❌ ما تم العثور على التوكن")
    exit()

bot = telebot.TeleBot(TOKEN)

print("✅ البوت شغال الآن...")

# أمر /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك 👋\nالبوت شغال 100% 🚀")

# أمر /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "📌 الأوامر:\n/start - تشغيل البوت\n/help - المساعدة")

# رد على أي رسالة
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"📩 رسالتك:\n{message.text}")

# تشغيل البوت
bot.infinity_polling()
