#import os
from typing import List
from openai import OpenAI
#from dotenv import load_dotenv
#load_dotenv()
from core.schema import SensorSignal
from ai.formatter import signals_to_text
from core.config import AI_KEY, GROQ_BASE_URL, AI_MODEL

client = OpenAI(
    api_key=AI_KEY,
    base_url=GROQ_BASE_URL
)

def analyze_signals(signals: List[SensorSignal]) -> str:
    """
    Анализирует сигналы с помощью ИИ.
    """

    context = signals_to_text(signals)

    prompt = f"""
Ты — технический аналитик системы мониторинга.

Проанализируй сигналы ниже и кратко ответь:
- есть ли проблемы
- есть ли риски
- что требует внимания

Сигналы:
{context}
"""

    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=[
            {"role": "system", "content": "Ты инженерный аналитик."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
