import telebot
from telebot.types import *
import time, json, os, datetime

TOKEN = "8632139720:AAFxaBKYXoYYijSBpIHeKPlfpMg1UmE47ws"
CHANNEL = "@bayram_vip"
ADMIN_ID = 8214596362

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"

# عناوينك
USDT_TRC20 = "TMviBrABzuAhy7ToHXXgH3qYUaTBynFwJU"
USDT_BEP20 = "0x5040f6e845e37dd40be20ea9e0af8c9cdb8c282b"
BTC_ADDRESS = "0x5040f6e845e37dd40be20ea9e0af8c9cdb8c282b"

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

# القوائم
def main_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("💰 أرباحي", "🎁 المهام")
    m.row("🎯 مكافأة يومية", "📊 سحب الأرباح")
    m.row("👥 دعوة الأصدقاء", "💳 إيداع")
    m.row("📅 التاريخ", "🆔 ايدي حسابي")
    m.row("☎️ تواصل معنا")
    return m

def back_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("🔙 رجوع")
    return m

# START
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
            bot.send_message(int(inviter), "🎉 دعوة جديدة +0.20$")

    save()

    if not check_sub(uid):
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📢 اشترك", url="https://t.me/bayram_vip"),
            InlineKeyboardButton("✅ تحقق", callback_data="check")
        )
        bot.send_message(uid, "🚫 اشترك بالقناة أولاً", reply_markup=markup)
        return

    bot.send_message(uid, "🔥 أهلاً بك في بوت VIP", reply_markup=main_menu())

# تحقق
@bot.callback_query_handler(func=lambda c: c.data == "check")
def check(call):
    if check_sub(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ تم التحقق", reply_markup=main_menu())
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك")

# رجوع
@bot.message_handler(func=lambda m: m.text == "🔙 رجوع")
def back(m):
    bot.send_message(m.chat.id, "رجعت للقائمة الرئيسية", reply_markup=main_menu())

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
    bot.send_message(m.chat.id,
                     "📢 ادخل القناة وتصفح المنشورات ثم اضغط تنفيذ",
                     reply_markup=back_menu())

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

# الدعوة
@bot.message_handler(func=lambda m: m.text == "👥 دعوة الأصدقاء")
def invite(m):
    link = f"https://t.me/{bot.get_me().username}?start={m.from_user.id}"
    bot.send_message(m.chat.id,
                     f"👥 اربح 0.20$ لكل شخص\n\n🔗 رابطك:\n{link}")

# الإيداع
@bot.message_handler(func=lambda m: m.text == "💳 إيداع")
def deposit(m):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("USDT TRC20", callback_data="trx"),
        InlineKeyboardButton("USDT BEP20", callback_data="bsc")
    )
    markup.add(
        InlineKeyboardButton("BTC", callback_data="btc")
    )
    bot.send_message(m.chat.id, "اختر الشبكة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data in ["trx","bsc","btc"])
def deposit_show(call):
    if call.data == "trx":
        addr = USDT_TRC20
        net = "TRC20"
    elif call.data == "bsc":
        addr = USDT_BEP20
        net = "BEP20"
    else:
        addr = BTC_ADDRESS
        net = "BTC"

    bot.send_message(call.message.chat.id,
                     f"💳 الشبكة: {net}\n\n📥 عنوانك:\n`{addr}`\n\n⚠️ أرسل فقط على هذه الشبكة",
                     parse_mode="Markdown")

# التاريخ
@bot.message_handler(func=lambda m: m.text == "📅 التاريخ")
def date(m):
    now = datetime.datetime.now()
    bot.send_message(m.chat.id, f"📅 التاريخ:\n{now}")

# ID
@bot.message_handler(func=lambda m: m.text == "🆔 ايدي حسابي")
def myid(m):
    bot.send_message(m.chat.id, f"🆔 ID: {m.from_user.id}")

# السحب
@bot.message_handler(func=lambda m: m.text == "📊 سحب الأرباح")
def withdraw(m):
    u = get_user(m.from_user.id)

    if u["balance"] < 50:
        bot.send_message(m.chat.id, "❌ الحد الأدنى 50$")
        return

    bot.send_message(m.chat.id, "✍️ أرسل بياناتك للسحب")

# تشغيل
print("BOT RUNNING...")
bot.infinity_polling()
