import requests
CHANNEL_USERNAME = "@chafi9vip"
INSTAGRAM_URL = "https://www.instagram.com/old.chafii9?igsh=MWdheTh6Zm1tNTAxcg=="
def is_subscribed(bot, user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# 🔑 ضع التوكنات هنا
BOT_TOKEN = "8529085496:AAEgjI98ncStqDPat_q6UJ1Fc1HdgXrIjSg"
VT_API_KEY = "fc3789913edb1c49af793b4593f028166f9e4860e0dd7cadb9eef68577728a19"

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبًا!\nأرسل رابط موقع وسأفحصه لك 🔍"
    )

# فحص الرابط
async def check_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    headers = {
        "x-apikey": VT_API_KEY
    }
    data = {
        "url": url
    }

    # إرسال الرابط لـ VirusTotal
    response = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data=data
    )

    if response.status_code != 200:
        await update.message.reply_text("❌ حدث خطأ أثناء الفحص")
        return

    analysis_id = response.json()["data"]["id"]

    # جلب النتيجة
    report = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    if report.status_code != 200:
        await update.message.reply_text("❌ لم أستطع جلب نتيجة الفحص")
        return

    stats = report.json()["data"]["attributes"]["stats"]

    message = (
        "🔍 **نتيجة فحص الرابط**\n\n"
        f"✅ آمن: {stats.get('harmless', 0)}\n"
        f"⚠️ مشبوه: {stats.get('suspicious', 0)}\n"
        f"❌ خبيث: {stats.get('malicious', 0)}"
    )

    await update.message.reply_text(message, parse_mode="Markdown")

# تشغيل البوت
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_url))
    @bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if not is_subscribed(bot, user_id):
        bot.send_message(
            message.chat.id,
            "🚫 لا يمكنك استخدام البوت\n\n"
            "📢 اشترك في القناة أولًا:\n"
            f"{CHANNEL_USERNAME}\n\n"
            "📸 وتابع حسابنا على إنستغرام:\n"
            f"{INSTAGRAM_URL}\n\n"
            "✅ ثم أرسل /start من جديد"
        )
        return

    bot.send_message(message.chat.id, "✅ مرحبًا بك! يمكنك الآن استخدام البوت")

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
