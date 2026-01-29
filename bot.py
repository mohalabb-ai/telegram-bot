import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ====== ENV ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
VT_API_KEY = os.getenv("VT_API_KEY")
CHANNEL_USERNAME = os.getenv("@chafi9vip")
INSTAGRAM_URL = os.getenv("https://www.instagram.com/old.chafii9?igsh=MWdheTh6Zm1tNTAxcg==")


# ====== فحص الاشتراك ======
async def is_subscribed(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ====== رسالة الاشتراك ======
async def ask_for_subscription(update: Update):
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("📸 تابع إنستغرام", url=INSTAGRAM_URL)],
        [InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub")]
    ]
    await update.message.reply_text(
        "🚫 لا يمكنك استخدام البوت قبل:\n"
        "1️⃣ الاشتراك في القناة\n"
        "2️⃣ متابعة الإنستغرام\n\n"
        "ثم اضغط ✅ تحقق",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ====== /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_subscribed(context.bot, user_id):
        await ask_for_subscription(update)
        return

    await update.message.reply_text(
        "👋 مرحبًا بك!\n"
        "🔗 أرسل رابطًا وسأفحصه لك 🔍"
    )


# ====== فحص الرابط ======
async def check_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_subscribed(context.bot, user_id):
        await ask_for_subscription(update)
        return

    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("❗ أرسل رابطًا صحيحًا يبدأ بـ http أو https")
        return

    headers = {"x-apikey": VT_API_KEY}
    data = {"url": url}

    try:
        submit = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data=data,
            timeout=15
        )

        analysis_id = submit.json()["data"]["id"]

        report = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers,
            timeout=15
        )

        stats = report.json()["data"]["attributes"]["stats"]

        message = (
            "🔍 **نتيجة فحص الرابط**\n\n"
            f"✅ آمن: {stats.get('harmless', 0)}\n"
            f"⚠️ مشبوه: {stats.get('suspicious', 0)}\n"
            f"❌ خبيث: {stats.get('malicious', 0)}"
        )

        await update.message.reply_text(message, parse_mode="Markdown")

    except:
        await update.message.reply_text("❌ حدث خطأ أثناء فحص الرابط")


# ====== MAIN ======
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_url))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
