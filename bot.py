from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# 🔥 KEEP ALIVE (مهم)
from flask import Flask
from threading import Thread

app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot is running!"

def run():
    app_web.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🔐 التوكن
TOKEN = "8632139720:AAFxaBKYXoYYijSBpIHeKPlfpMg1UmE47ws"

CHANNEL_USERNAME = "@bayram_vip"
CHANNEL_LINK = "https://t.me/bayram_vip"

SUPPORT = "@Gold_3id"
SUPPORT_ID = "8214596362"

# المحافظ
USDT_TRC20 = "TMviBrABzuAhy7ToHXXgH3qYUaTByFwJU"
USDT_BEP20 = "0x5040f6e845e37dd40be20ea9e0af8c9cdb8c282b"
BTC = "0x5040f6e845e37dd40be20ea9e0af8c9cdb8c282b"

# الواجهة
main_keyboard = ReplyKeyboardMarkup([
    ["💰 أرباحي", "🎁 المهام"],
    ["🎯 مكافأة يومية", "📊 سحب الأرباح"],
    ["👥 دعوة الأصدقاء", "💳 إيداع"],
    ["📅 التاريخ", "🆔 معرفة ID"],
    ["📞 تواصل مع الإدارة"]
], resize_keyboard=True)

deposit_keyboard = ReplyKeyboardMarkup([
    ["USDT TRC20", "USDT BEP20"],
    ["BTC"],
    ["🔙 رجوع"]
], resize_keyboard=True)

withdraw_keyboard = ReplyKeyboardMarkup([
    ["🏦 حوالة بنكية", "💳 Payeer"],
    ["💰 Perfect Money", "📱 Vodafone Cash"],
    ["📱 Syriatel Cash", "📱 MTN Cash"],
    ["🇮🇶 زين كاش", "🇸🇾 حوالة محلية"],
    ["💵 شام كاش"],
    ["💲 USDT", "🪙 Bitcoin"],
    ["🔙 رجوع"]
], resize_keyboard=True)

# تحقق الاشتراك
async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if not await is_subscribed(user_id, context):
        await update.message.reply_text(
            f"🚫 اشترك أولاً:\n{CHANNEL_LINK}\nثم أرسل /start"
        )
        return

    await update.message.reply_text(
        f"""🔥 أهلاً بك في بوت الأرباح 🔥

💸 اربح يومياً بسهولة
👥 زيد أرباحك بدعوة الأصدقاء
🚀 نظام ذكي وتحديث مستمر

📞 الدعم: {SUPPORT}""",
        reply_markup=main_keyboard
    )

# التاريخ
def get_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), "تقريبي: 1447 هـ"

# الردود
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if not await is_subscribed(user_id, context):
        await update.message.reply_text(
            f"🚫 اشترك أولاً:\n{CHANNEL_LINK}\nثم /start"
        )
        return

    if text == "💳 إيداع":
        await update.message.reply_text("💰 اختر:", reply_markup=deposit_keyboard)

    elif text == "USDT TRC20":
        await update.message.reply_text(USDT_TRC20)

    elif text == "USDT BEP20":
        await update.message.reply_text(USDT_BEP20)

    elif text == "BTC":
        await update.message.reply_text(BTC)

    elif text == "🎁 المهام":
        await update.message.reply_text(
            f"📢 ادخل القناة:\n{CHANNEL_LINK}\nثم تفاعل"
        )

    elif text == "📊 سحب الأرباح":
        await update.message.reply_text("اختر:", reply_markup=withdraw_keyboard)

    elif text in ["🏦 حوالة بنكية","💳 Payeer","💰 Perfect Money","📱 Vodafone Cash",
                  "📱 Syriatel Cash","📱 MTN Cash","🇮🇶 زين كاش","🇸🇾 حوالة محلية",
                  "💵 شام كاش","💲 USDT","🪙 Bitcoin"]:
        await update.message.reply_text("❌ أكمل المهام + دعوة أصدقاء")

    elif text == "👥 دعوة الأصدقاء":
        await update.message.reply_text(
            f"https://t.me/YOUR_BOT?start={user_id}"
        )

    elif text == "🎯 مكافأة يومية":
        await update.message.reply_text("تم إضافة 0.10$")

    elif text == "💰 أرباحي":
        await update.message.reply_text("رصيدك: 0.00$")

    elif text == "📅 التاريخ":
        g,h = get_date()
        await update.message.reply_text(f"{g}\n{h}")

    elif text == "🆔 معرفة ID":
        await update.message.reply_text(f"ID: {user_id}")

    elif text == "📞 تواصل مع الإدارة":
        await update.message.reply_text(f"{SUPPORT}\nID: {SUPPORT_ID}")

    elif text == "🔙 رجوع":
        await update.message.reply_text("رجوع", reply_markup=main_keyboard)

# تشغيل
keep_alive()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

print("🔥 BOT RUNNING...")
app.run_polling()
