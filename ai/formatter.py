from typing import List
from core.schema import SensorSignal


def signals_to_text(signals: List[SensorSignal]) -> str:
    """
    Преобразует сигналы в текст для ИИ.
    """

    blocks = []

    for s in signals:
        block = (
            f"Сенсор: {s.sensor}\n"
            f"Статус: {s.status}\n"
            f"Сообщение: {s.message}\n"
            f"Данные: {s.data}\n"
        )
        blocks.append(block)

    return "\n---\n".join(blocks)
