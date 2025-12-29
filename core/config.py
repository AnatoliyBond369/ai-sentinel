import os
from dotenv import load_dotenv

# Загружаем .env ОДИН РАЗ
load_dotenv()

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Переменная окружения {name} не задана")
    return value

# === API ключи ===
AI_KEY = require_env("AI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")  # необязательный

# === AI ===
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
AI_MODEL = "llama-3.3-70b-versatile"

# === Пороги сенсоров ===
STOCK_ALERT_THRESHOLD = 5.0  # %
GCP_LATENCY_WARNING_MS = 1000
