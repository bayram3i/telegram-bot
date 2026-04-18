from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import sqlite3

TOKEN = "8705956398:AAG6YbKmjsAolqg-dBo0IqWQk3UCOTDwbUI"

# 💰 عناوينك
BEP20 = "0x5040f6e845e37dd40be20ea9e0af8c9cdb8c282b"
TRC20 = "TMviBrABzuAhy7ToHXXgH3qYUaTBynFwJU"

# 📞 تواصل
CONTACT = "@Bayram43ie"

# ======================
# DATABASE
# ======================
conn = sqlite3.connect("donation.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    donations INTEGER DEFAULT 0
)
""")
conn.commit()

def add_user(user_id):
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def add_donation(user_id):
    cur.execute("UPDATE users SET donations = donations + 1 WHERE user_id=?", (user_id,))
    conn.commit()

def get_donation(user_id):
    cur.execute("SELECT donations FROM users WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else 0

# ======================
# START UI
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id)

    keyboard = [
        [InlineKeyboardButton("💰 تبرع الآن", callback_data="donate")],
        [InlineKeyboardButton("📊 تبرعاتي", callback_data="stats")],
        [InlineKeyboardButton("📞 تواصل معنا", url=f"https://t.me/{CONTACT.replace('@','')}")]
    ]

    await update.message.reply_text(
        f"✨ أهلاً بك {user.first_name}\n\n"
        "🤍 مرحباً بك في منصة التبرعات\n\n"
        "💡 تبرعك يساعد في دعم المحتاجين\n"
        "اختر من الخيارات بالأسفل 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ======================
# BUTTONS
# ======================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # 💰 صفحة التبرع
    if query.data == "donate":
        keyboard = [
            [InlineKeyboardButton("📥 BEP20", callback_data="bep20")],
            [InlineKeyboardButton("📥 TRC20", callback_data="trc20")],
            [InlineKeyboardButton("✅ تم التبرع", callback_data="done")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")]
        ]

        await query.message.reply_text(
            "💰 اختر طريقة التبرع:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # BEP20
    elif query.data == "bep20":
        await query.message.reply_text(
            f"📥 عنوان BEP20:\n\n{BEP20}\n\n📋 انسخ العنوان وقم بالتحويل"
        )

    # TRC20
    elif query.data == "trc20":
        await query.message.reply_text(
            f"📥 عنوان TRC20:\n\n{TRC20}\n\n📋 انسخ العنوان وقم بالتحويل"
        )

    # تأكيد التبرع
    elif query.data == "done":
        add_donation(user_id)

        await query.message.reply_text(
            "🙏 شكراً لتبرعك\n🤍 سيتم مراجعته\n🌟 جزاك الله خير"
        )

    # الإحصائيات
    elif query.data == "stats":
        total = get_donation(user_id)

        await query.message.reply_text(
            f"📊 عدد مرات تبرعك:\n💰 {total}"
        )

    # رجوع
    elif query.data == "back":
        await start(update, context)

# ======================
# RUN
# ======================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Donation UI Bot Running...")
app.run_polling()
