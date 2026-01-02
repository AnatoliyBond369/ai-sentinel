# bot/handlers.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

# Импорты твоих модулей
from aggregator.sensor_aggregator import run_all_sensors
from ai.analyzer import analyze_signals

logger = logging.getLogger(__name__)

def get_main_keyboard():
    """Создает интерактивную кнопку под сообщением"""
    keyboard = [[InlineKeyboardButton("⚡️ Запустить полный анализ", callback_data="run_analysis")]]
    return InlineKeyboardMarkup(keyboard)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие при команде /start"""
    await update.message.reply_text(
        "👋 <b>Добро пожаловать в AI Sentinel!</b>\n\n"
        "Я система автономного мониторинга инфраструктуры GCP и рынка Alphabet.\n"
        "Нажмите кнопку ниже, чтобы получить мгновенный отчет.",
        parse_mode='HTML',
        reply_markup=get_main_keyboard()
    )

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Основной обработчик: срабатывает на /status и на нажатие кнопки.
    """
    # 1. Определяем, откуда пришел запрос (команда или кнопка)
    query = update.callback_query
    
    if query:
        await query.answer() # Убираем "часики" на кнопке
        chat_id = query.message.chat.id
        # Сообщаем о начале работы, редактируя старое сообщение или отправляя новое
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    else:
        chat_id = update.effective_chat.id
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        await update.message.reply_text("⌛ <b>Sentinel:</b> Сбор данных...")

    try:
        # 2. Сбор данных (Aggregator)
        signals = run_all_sensors()
        
        # 3. ИИ Анализ
        ai_verdict = analyze_signals(signals)

        # 4. Формирование прозрачного отчета (Модель: Данные + ИИ)
        sensor_blocks = []
        for s in signals:
            emoji = "🟢" if s.status == "ok" else "🟡" if s.status == "warning" else "🔴"
            sensor_blocks.append(f"{emoji} <b>{s.sensor}:</b> {s.status.upper()}\n∟ {s.message}")

        # Берем временную метку из первого сигнала
        ts = signals[0].timestamp if signals else "N/A"

        report_text = (
            f"🛰 <b>AI SENTINEL: СТАТУС СИСТЕМЫ</b>\n"
            f"📅 <i>{ts}</i>\n\n"
            f"{'\n\n'.join(sensor_blocks)}\n\n"
            f"🤖 <b>ВЕРДИКТ ИИ:</b>\n{ai_verdict}"
        )

        # 5. Отправка результата (всегда прикрепляем кнопку для повтора)
        if query:
            # Если нажата кнопка, редактируем сообщение (чтобы не спамить в чате)
            await query.edit_message_text(report_text, parse_mode='HTML', reply_markup=get_main_keyboard())
        else:
            # Если введена команда текстом
            await update.message.reply_text(report_text, parse_mode='HTML', reply_markup=get_main_keyboard())

    except Exception as e:
        logger.error(f"Ошибка в status_handler: {e}")
        error_msg = f"❌ <b>Ошибка анализа:</b>\n{str(e)}"
        if query:
            await query.message.reply_text(error_msg, parse_mode='HTML')
        else:
            await update.message.reply_text(error_msg, parse_mode='HTML')
