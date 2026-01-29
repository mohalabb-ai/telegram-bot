import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================== الإعدادات ==================

BOT_TOKEN = os.getenv("BOT_TOKEN")
SAFE_KEY = os.getenv("SAFE_BROWSING_KEY")

# يوزر قناتك في تيليغرام (بدون @)
TELEGRAM_CHANNEL = "your_telegram_channel"

# رابط قناة الانستغرام
INSTAGRAM_LINK = "https://www.instagram.com/your_instagram/"

# ===============================================


# ---------- فحص الاشتراك ----------
async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(
            chat_id=f"@{TELEGRAM_CHANNEL}",
            user_id=user_id
        )
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ---------- فحص الرابط ----------
def check_url(url):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={SAFE_KEY}"

    payload = {
        "client": {
            "clientId": "telegram-bot",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    response = requests.post(endpoint, json=payload)
    data = response.json()

    return "matches" in data


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    subscribed = await is_subscribed(user_id, context)

    if not subscribed:
        await update.message.reply_text(
            "🚫 لاستخدام البوت يجب الاشتراك أولاً:\n\n"
            f"📢 قناة تيليغرام:\nhttps://t.me/{TELEGRAM_CHANNEL}\n\n"
            f"📸 قناة إنستغرام:\n{INSTAGRAM_LINK}\n\n"
            "✅ بعد الاشتراك أرسل /start"
        )
        return

    await update.message.reply_text(
        "✅ أهلاً بك!\n\n"
        "🔗 أرسل أي رابط وسأفحصه لك هل هو ملغّم أم لا."
    )


# ---------- استقبال الروابط ----------
async def scan_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    subscribed = await is_subscribed(user_id, context)
    if not subscribed:
        await update.message.reply_text(
            "🚫 يجب الاشتراك في القناة أولاً لاستخدام البوت.\n"
            f"https://t.me/{TELEGRAM_CHANNEL}"
        )
        return

    text = update.message.text

    if "http://" in text or "https://" in text:
        dangerous = check_url(text)

        if dangerous:
            await update.message.reply_text(
                "❌ تحذير!\n"
                "هذا الرابط ملغّم أو تصيّد 🚫"
            )
        else:
            await update.message.reply_text(
                "✅ الرابط آمن حسب الفحص 🔍"
            )


# ---------- التشغيل ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, scan_links))

    app.run_polling()


if __name__ == "__main__":
    main()
