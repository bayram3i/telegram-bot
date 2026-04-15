from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

TOKEN = "8632139720:AAFxaBKYXoYYijSBpIHeKPlfpMg1UmE47ws"

CHANNEL_USERNAME = "@bayram_vip"
CHANNEL_LINK = "https://t.me/bayram_vip"

SUPPORT = "@Gold_3id"
SUPPORT_ID = "8214596362"

# المحافظ
USDT_TRC20 = "TMviBrABzuAhy7ToHXXgH3qYUaTByFwJU"
USDT_BEP20 = "0x5040f6e845e37dd40be20ea9e0af8c9cdb8c282b"
BTC = "0x5040f6e845e37dd40be20ea9e0af8c9cdb8c282b"

# القوائم
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
            f"🚫 يجب الاشتراك أولاً في القناة:\n{CHANNEL_LINK}\n\n"
            "ثم أعد إرسال /start"
        )
        return

    await update.message.reply_text(
        "🔥 مرحباً بك في بوت الأرباح الاحترافي 🔥\n\n"
        "💸 اربح يومياً من المهام\n"
        "🚀 نظام سريع وآمن\n\n"
        f"📞 الدعم: {SUPPORT}",
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

    # منع الاستخدام بدون اشتراك
    if not await is_subscribed(user_id, context):
        await update.message.reply_text(
            f"🚫 يجب الاشتراك أولاً:\n{CHANNEL_LINK}\n\n"
            "ثم أرسل /start"
        )
        return

    # الإيداع
    if text == "💳 إيداع":
        await update.message.reply_text("💰 اختر طريقة الإيداع:", reply_markup=deposit_keyboard)

    elif text == "USDT TRC20":
        await update.message.reply_text(f"💰 عنوان TRC20:\n{USDT_TRC20}")

    elif text == "USDT BEP20":
        await update.message.reply_text(f"💰 عنوان BEP20:\n{USDT_BEP20}")

    elif text == "BTC":
        await update.message.reply_text(f"💰 عنوان BTC:\n{BTC}")

    # المهام
    elif text == "🎁 المهام":
        await update.message.reply_text(
            f"📢 المهام اليومية:\n\n"
            f"1️⃣ الدخول للقناة:\n{CHANNEL_LINK}\n"
            f"2️⃣ الاشتراك\n"
            f"3️⃣ التفاعل مع المنشورات\n\n"
            f"🎁 بعد الإكمال تحصل على أرباح\n\n"
            f"📞 الدعم: {SUPPORT}"
        )

    # السحب
    elif text == "📊 سحب الأرباح":
        await update.message.reply_text("💸 اختر طريقة السحب:", reply_markup=withdraw_keyboard)

    elif text in ["🏦 حوالة بنكية", "💳 Payeer", "💰 Perfect Money", "📱 Vodafone Cash",
                  "📱 Syriatel Cash", "📱 MTN Cash", "🇮🇶 زين كاش", "🇸🇾 حوالة محلية",
                  "💵 شام كاش", "💲 USDT", "🪙 Bitcoin"]:
        await update.message.reply_text(
            f"💳 طريقة السحب: {text}\n\n"
            "❌ لا يمكن السحب حالياً\n"
            "⚠️ يجب إكمال المهام + دعوة أصدقاء\n\n"
            f"📞 تواصل مع الإدارة: {SUPPORT}"
        )

    # الدعوات
    elif text == "👥 دعوة الأصدقاء":
        await update.message.reply_text(
            f"🔗 رابطك:\nhttps://t.me/YOUR_BOT?start={user_id}\n\n"
            "💸 اربح 0.20$ لكل شخص"
        )

    # المكافأة
    elif text == "🎯 مكافأة يومية":
        await update.message.reply_text("🎯 تمت إضافة 0.10$ إلى حسابك")

    # الأرباح
    elif text == "💰 أرباحي":
        await update.message.reply_text("💰 رصيدك الحالي: 0.00$")

    # التاريخ
    elif text == "📅 التاريخ":
        g, h = get_date()
        await update.message.reply_text(
            f"📅 التاريخ:\n\n📆 ميلادي: {g}\n🌙 هجري: {h}"
        )

    # ID المستخدم
    elif text == "🆔 معرفة ID":
        await update.message.reply_text(
            f"🆔 ID حسابك:\n{user_id}\n\n"
            f"📞 تواصل مع الإدارة: {SUPPORT}"
        )

    # التواصل
    elif text == "📞 تواصل مع الإدارة":
        await update.message.reply_text(
            f"📞 تواصل مع الإدارة مباشرة:\n\n"
            f"👤 {SUPPORT}\n"
            f"🆔 ID: {SUPPORT_ID}"
        )

    # رجوع
    elif text == "🔙 رجوع":
        await update.message.reply_text("🔙 رجعت للقائمة الرئيسية", reply_markup=main_keyboard)


# تشغيل
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

print("BOT RUNNING...")
app.run_polling()
