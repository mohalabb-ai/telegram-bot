import os
import requests
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# عدلهم 👇
CHANNEL_USERNAME = "@chafi9vip"
INSTAGRAM_URL = "https://instagram.com/old.chafii9"

# ====== check subscription ======
async def is_subscribed(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ====== force subscribe message ======
async def force_subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("📸 تابعنا على إنستغرام", url=INSTAGRAM_URL)],
        [InlineKeyboardButton("✅ تحققت من الاشتراك", callback_data="check")]
    ]
    await update.message.reply_text(
        "🚫 لا يمكنك استخدام البوت قبل الاشتراك:\n\n"
        "1️⃣ اشترك في قناة تيليغرام\n"
        "2️⃣ تابعنا على إنستغرام\n\n"
        "ثم اضغط (تحققت من الاشتراك)",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ====== start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot = context.bot

    if not await is_subscribed(bot, user_id):
        await force_subscribe(update, context)
        return

    await update.message.reply_text(
        "✅ مرحبًا بك!\n\n"
        "🔗 أرسل الرابط وسأقوم بفحصه."
    )

# ====== link checker ======
async def check_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot = context.bot

    if not await is_subscribed(bot, user_id):
        await force_subscribe(update, context)
        return

    text = update.message.text

    if not text.startswith("http"):
        return

    # فحص بسيط (تحذير مبدئي)
    if any(word in text.lower() for word in ["login", "free", "verify", "bonus"]):
        await update.message.reply_text("⚠️ تحذير: الرابط **مشبوه**، كن حذرًا.")
    else:
        await update.message.reply_text("✅ لا يوجد شيء خطير ظاهر في الرابط.")

# ====== main ======
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_link))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
