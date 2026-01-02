# bot/telegram_bot.py
from telegram.ext import ApplicationBuilder, CommandHandler,CallbackQueryHandler
from bot.handlers import status_handler,start_handler
from core import config 
def create_bot():
    # Используем config.BOT_TOKEN напрямую
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CallbackQueryHandler(status_handler, pattern="run_analysis"))
    return app
