# main.py
import sys
from bot.telegram_bot import create_bot
#from core.config import Config
from core import config

def start_sentinel():
    """
    Запуск асинхронного бота AI Sentinel.
    """
    print("🤖 Бот AI Sentinel инициализируется...")

    # 1. Валидация конфигурации
    if not config.BOT_TOKEN:
        print("❌ КРИТИЧЕСКАЯ ОШИБКА: TELEGRAM_TOKEN не найден в .env!")
        sys.exit(1)
    
    if not config.AI_KEY:
        print("⚠️ ПРЕДУПРЕЖДЕНИЕ: AI_KEY не найден. ИИ будет работать в режиме симуляции.")

    # 2. Создание приложения
    # Функция create_bot() должна быть в bot/telegram_bot.py
    app = create_bot()

    print("✅ Бот успешно запущен в режиме Polling.")
    print("👉 Напиши /status в Telegram для проверки системы.")

    # 3. Запуск бесконечного цикла опроса Telegram
    app.run_polling()

if __name__ == "__main__":
    start_sentinel()
