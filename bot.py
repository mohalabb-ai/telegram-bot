import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN") 
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing")
VT_API_KEY = os.getenv("VT_API_KEY")
if not VT_API_KEY:
    raise ValueError("VT_API_KEY is missing")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
INSTAGRAM_URL = os.getenv("INSTAGRAM_URL")


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
from telegram.ext import MessageHandler, filters
from telegram.ext import CommandHandler

async def start(update, context):
    await update.message.reply_text(
        "👋 أهلاً بك!\n"
        "أرسل أي رابط وسأفحصه لك 🔍"
    )

app.add_handler(CommandHandler("start", start))

# ===== فحص الرابط =====
import asyncio
import requests
from telegram import Update
from telegram.ext import ContextTypes

async def check_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    headers = {
        "x-apikey": VT_API_KEY
    }

    # إرسال الرابط
    response = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data={"url": url}
    )

    if response.status_code != 200:
        await update.message.reply_text("❌ فشل إرسال الرابط إلى VirusTotal")
        return

    analysis_id = response.json()["data"]["id"]

    await update.message.reply_text("⏳ جاري فحص الرابط، انتظر قليلًا...")

    # ⏳ انتظر 15 ثانية
    await asyncio.sleep(15)

    # جلب النتيجة
    report = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    if report.status_code != 200:
        await update.message.reply_text("❌ فشل جلب نتيجة الفحص")
        return

    stats = report.json()["data"]["attributes"]["stats"]

    message = (
        "🔍 **نتيجة فحص الرابط**\n\n"
        f"✅ آمن: {stats.get('harmless', 0)}\n"
        f"⚠️ مشبوه: {stats.get('suspicious', 0)}\n"
        f"❌ خبيث: {stats.get('malicious', 0)}"
    )

    await update.message.reply_text(message, parse_mode="Markdown")


# ===== التشغيل =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_url))

    app.run_polling()


if __name__ == "__main__":
    main()
