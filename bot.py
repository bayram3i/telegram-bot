import telebot

TOKEN = "8581997484:AAGhu3zwL5lmrqhOL2jXKUjXwfBajpT0Qu0"

bot = telebot.TeleBot(TOKEN)

print("✅ البوت شغال")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "البوت شغال 100% 🚀")

bot.infinity_polling()
