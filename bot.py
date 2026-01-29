import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("8529085496:AAEgjI98ncStqDPat_q6UJ1Fc1HdgXrIjSg")

CHANNEL_USERNAME = "@chafi9vip"
INSTAGRAM_URL = "https://www.instagram.com/old.chafi9"


async def is_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_subscribed(user_id, context):
        await update.message.reply_text(
            "🚫 يجب الاشتراك أولًا\n\n"
            f"📢 قناة تيليغرام:\n{CHANNEL_USERNAME}\n\n"
            f"📸 إنستغرام:\n{INSTAGRAM_URL}\n\n"
            "✅ بعد الاشتراك أرسل /start"
        )
        return

    await update.message.reply_text("✅ أهلاً بك، تم تفعيل البوت بنجاح!")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()


if name == "__main__":
    main()
