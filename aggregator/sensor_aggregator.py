# aggregator/sensor_aggregator.py

from typing import List

from sensors.stock_sensor import run_stock_sensor
from sensors.gcp_sensor import run_gcp_sensor
from core.schema import SensorSignal


def run_all_sensors() -> List[SensorSignal]:
    """
    Запускает все доступные сенсоры и
    возвращает список сигналов.
    """

    signals: List[SensorSignal] = []

    # 1. Сенсор рынка
    stock_signal = run_stock_sensor("AAPL")
    signals.append(stock_signal)

    # 2. Сенсор доступности сервиса
    gcp_signal = run_gcp_sensor("https://www.google.com")
    signals.append(gcp_signal)

    return signals
