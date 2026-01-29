import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
VT_API_KEY = os.getenv("VT_API_KEY")
CHANNEL_USERNAME = os.getenv("@chafi9vip")
INSTAGRAM_URL = os.getenv("https://www.instagram.com/old.chafii9?igsh=MWdheTh6Zm1tNTAxcg==")


# ===== فحص الاشتراك =====
async def is_subscribed(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False


# ===== رسالة الاشتراك =====
async def ask_sub(update: Update):
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("📸 تابع إنستغرام", url=INSTAGRAM_URL)]
    ]
    await update.message.reply_text(
        "🚫 يجب الاشتراك قبل استخدام البوت",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_subscribed(context.bot, user_id):
        await ask_sub(update)
        return

    await update.message.reply_text("🔗 أرسل الرابط لفحصه")


# ===== فحص الرابط =====
async def check_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_subscribed(context.bot, user_id):
        await ask_sub(update)
        return

    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("❗ أرسل رابطًا صحيحًا")
        return

    headers = {"x-apikey": VT_API_KEY}
    data = {"url": url}

    try:
        r = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data=data)
        analysis_id = r.json()["data"]["id"]

        report = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers
        )

        stats = report.json()["data"]["attributes"]["stats"]

        msg = (
            "🔍 نتيجة الفحص:\n\n"
            f"✅ آمن: {stats['harmless']}\n"
            f"⚠️ مشبوه: {stats['suspicious']}\n"
            f"❌ خبيث: {stats['malicious']}"
        )

        await update.message.reply_text(msg)

    except:
        await update.message.reply_text("❌ فشل الفحص")


# ===== التشغيل =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_url))

    app.run_polling()


if __name__ == "__main__":
    main()
