import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue

# فعال کردن لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# توکن ربات از فایل .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logging.error("❌ توکن ربات پیدا نشد! فایل .env را بررسی کنید.")
    exit(1)

# این ID چت شماست. آن را با ID چت خود جایگزین کنید.
YOUR_CHAT_ID = "YOUR_CHAT_ID"

async def send_alive_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """هر ۵ دقیقه پیام "من زنده‌ام" را ارسال می‌کند."""
    job = context.job
    await context.bot.send_message(
        chat_id=job.chat_id,
        text="من زنده‌ام! 🤖"
    )

def start_alive_job(chat_id: str, job_queue: JobQueue) -> None:
    """کار ارسال پیام را به JobQueue اضافه می‌کند."""
    # ارسال پیام هر ۵ دقیقه
    job_queue.run_repeating(
        send_alive_message,
        interval=300, # 300 ثانیه = ۵ دقیقه
        first=5,
        chat_id=chat_id,
        name=str(chat_id)
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """تابع مدیریت دستور /start"""
    user = update.effective_user
    chat_id = update.effective_chat.id

    # نمایش Chat ID به کاربر
    await update.message.reply_html(
        f"سلام {user.mention_html()}! من شروع به کار کردم. \n"
        f"Chat ID شما: <code>{chat_id}</code>"
    )

    # شروع کار ارسال پیام
    start_alive_job(chat_id, context.job_queue)

def main() -> None:
    """تابع اصلی ربات"""
    # ساخت اپلیکیشن
    application = Application.builder().token(BOT_TOKEN).build()
    
    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))

    # شروع ربات
    logging.info("ربات شروع به کار کرد...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()