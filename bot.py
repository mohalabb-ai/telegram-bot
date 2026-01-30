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

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
VT_API_KEY = os.getenv("VT_API_KEY")

CHANNEL_USERNAME = "@chafi9vip"
INSTAGRAM_URL = "https://www.instagram.com/old.chafii9?igsh=MWdheTh6Zm1tNTAxcg=="
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
VT_API_KEY = os.getenv("VT_API_KEY")

CHANNEL_USERNAME = "@YourChannel"
INSTAGRAM_URL = "https://instagram.com/old.chafii9"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing")

if not VT_API_KEY:
    raise ValueError("VT_API_KEY is missing")

# ================== SUB CHECK ==================
async def is_subscribed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ================== FORCE SUB ==================
async def force_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("📸 تابعنا على إنستغرام", url=INSTAGRAM_URL)],
        [InlineKeyboardButton("✅ تحققت", callback_data="check_sub")]
    ]
    await update.message.reply_text(
        "⚠️ يجب الاشتراك أولاً لاستخدام البوت:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================== /start ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_subscribed(update, context):
        await force_sub(update, context)
        return

    await update.message.reply_text(
        "👋 أهلاً بك\n"
        "🔗 أرسل رابطاً وسأفحصه لك"
    )

# ================== CHECK URL ==================
async def check_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_subscribed(update, context):
        await force_sub(update, context)
        return

    url = update.message.text.strip()

    headers = {"x-apikey": VT_API_KEY}
    data = {"url": url}

    r = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data=data
    )

    if r.status_code != 200:
        await update.message.reply_text("❌ فشل فحص الرابط")
        return

    analysis_id = r.json()["data"]["id"]

    analysis = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    stats = analysis.json()["data"]["attributes"]["stats"]

    await update.message.reply_text(
        f"✅ نتيجة الفحص:\n"
        f"🦠 ضار: {stats['malicious']}\n"
        f"⚠️ مشبوه: {stats['suspicious']}\n"
        f"✔️ آمن: {stats['harmless']}"
    )

# ================== MAIN ==================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_url))

    app.run_polling()

if __name__ == "__main__":
    main()

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing")

if not VT_API_KEY:
    raise ValueError("VT_API_KEY is missing")

# ================== SUB CHECK ==================
async def is_subscribed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ================== FORCE SUB ==================
async def force_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("📸 تابعنا على إنستغرام", url=INSTAGRAM_URL)],
        [InlineKeyboardButton("✅ تحققت", callback_data="check_sub")]
    ]
    await update.message.reply_text(
        "⚠️ يجب الاشتراك أولاً لاستخدام البوت:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================== /start ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_subscribed(update, context):
        await force_sub(update, context)
        return

    await update.message.reply_text(
        "👋 أهلاً بك\n"
        "🔗 أرسل رابطاً وسأفحصه لك"
    )

# ================== CHECK URL ==================
async def check_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_subscribed(update, context):
        await force_sub(update, context)
        return

    url = update.message.text.strip()

    headers = {"x-apikey": VT_API_KEY}
    data = {"url": url}

    r = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data=data
    )

    if r.status_code != 200:
        await update.message.reply_text("❌ فشل فحص الرابط")
        return

    analysis_id = r.json()["data"]["id"]

    analysis = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    stats = analysis.json()["data"]["attributes"]["stats"]

    await update.message.reply_text(
        f"✅ نتيجة الفحص:\n"
        f"🦠 ضار: {stats['malicious']}\n"
        f"⚠️ مشبوه: {stats['suspicious']}\n"
        f"✔️ آمن: {stats['harmless']}"
    )

# ================== MAIN ==================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_url))

    app.run_polling()

if __name__ == "__main__":
    main()
