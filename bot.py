import telebot
from telebot.types import *
import time, json, os, threading

TOKEN = os.getenv("8632139720:AAFxaBKYXoYYijSBpIHeKPlfpMg1UmE47ws")  # مهم ل Render
CHANNEL = "@bayram_vip"
ADMIN = "@Gold_3id"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

DATA_FILE = "data.json"

# تحميل البيانات
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

def save():
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

def get_user(uid):
    uid = str(uid)
    if uid not in users:
        users[uid] = {
            "balance": 0.0,
            "last_daily": 0,
            "last_task": 0,
            "invites": 0,
            "invited_by": None
        }
    return users[uid]

# تحقق الاشتراك
def check_sub(user_id):
    try:
        status = bot.get_chat_member(CHANNEL, user_id)
        return status.status in ["member", "creator", "administrator"]
    except:
        return False

DAY = 86400

# القائمة
def main_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("💰 أرباحي", "🎁 المهام")
    m.row("🎯 مكافأة يومية", "📊 سحب الأرباح")
    m.row("👥 دعوة الأصدقاء", "☎️ تواصل معنا")
    return m

# start
@bot.message_handler(commands=['start'])
def start(msg):
    uid = msg.from_user.id
    user = get_user(uid)

    args = msg.text.split()

    if len(args) > 1:
        inviter = args[1]
        if inviter != str(uid) and inviter in users and user["invited_by"] is None:
            user["invited_by"] = inviter
            users[inviter]["balance"] += 0.20
            users[inviter]["invites"] += 1

            bot.send_message(int(inviter), "🎉 شخص دخل من رابطك +0.20$")

    save()

    if not check_sub(uid):
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📢 اشترك", url="https://t.me/bayram_vip"),
            InlineKeyboardButton("✅ تحقق", callback_data="check")
        )
        bot.send_message(uid, "🚫 يجب الاشتراك بالقناة أولاً", reply_markup=markup)
        return

    bot.send_message(uid, "👋 أهلاً بك في بوت الربح 💸", reply_markup=main_menu())

# تحقق
@bot.callback_query_handler(func=lambda c: c.data == "check")
def check(call):
    if check_sub(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ تم التحقق", reply_markup=main_menu())
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك")

# أرباحي
@bot.message_handler(func=lambda m: m.text == "💰 أرباحي")
def balance(m):
    u = get_user(m.from_user.id)
    bot.send_message(m.chat.id,
                     f"💰 رصيدك: {u['balance']}$\n👥 دعواتك: {u['invites']}")

# مكافأة يومية
@bot.message_handler(func=lambda m: m.text == "🎯 مكافأة يومية")
def daily(m):
    u = get_user(m.from_user.id)
    now = time.time()

    if now - u["last_daily"] < DAY:
        bot.send_message(m.chat.id, "⏳ استلمتها اليوم")
        return

    u["balance"] += 0.10
    u["last_daily"] = now
    save()

    bot.send_message(m.chat.id, "🎉 +0.10$")

# المهام
@bot.message_handler(func=lambda m: m.text == "🎁 المهام")
def tasks(m):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📢 تنفيذ المهمة")
    markup.row("🔙 رجوع")

    bot.send_message(m.chat.id, "📢 تفاعل بالقناة ثم نفذ", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📢 تنفيذ المهمة")
def do_task(m):
    u = get_user(m.from_user.id)
    now = time.time()

    if not check_sub(m.from_user.id):
        bot.send_message(m.chat.id, "❌ اشترك أولاً")
        return

    if now - u["last_task"] < DAY:
        bot.send_message(m.chat.id, "⏳ نفذت اليوم")
        return

    u["balance"] += 0.15
    u["last_task"] = now
    save()

    bot.send_message(m.chat.id, "✅ +0.15$")

# دعوة
@bot.message_handler(func=lambda m: m.text == "👥 دعوة الأصدقاء")
def invite(m):
    link = f"https://t.me/{bot.get_me().username}?start={m.from_user.id}"
    bot.send_message(m.chat.id, f"🔗 رابطك:\n{link}")

# سحب
@bot.message_handler(func=lambda m: m.text == "📊 سحب الأرباح")
def withdraw(m):
    u = get_user(m.from_user.id)

    if u["balance"] < 50:
        bot.send_message(m.chat.id, "❌ الحد الأدنى 50$")
        return

    bot.send_message(m.chat.id, "💸 تم إرسال طلبك للإدارة")

# تواصل
@bot.message_handler(func=lambda m: m.text == "☎️ تواصل معنا")
def contact(m):
    bot.send_message(m.chat.id, "📩 تواصل: @Gold_3id")

# 🔥 نظام إعادة تشغيل تلقائي
def run_bot():
    while True:
        try:
            print("BOT STARTED...")
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print("ERROR:", e)
            time.sleep(5)

# تشغيل البوت في Thread
threading.Thread(target=run_bot).start()

# إبقاء Render شغال (مهم)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

app.run(host='0.0.0.0', port=10000)
