# sensors/stock_sensor.py

import yfinance as yf
from core.schema import SensorSignal


def run_stock_sensor(ticker: str = "AAPL") -> SensorSignal:
    """
    Сенсор рынка акций.
    Проверяет дневное изменение цены.
    """

    try:
        # 1. Загружаем данные по тикеру
        stock = yf.Ticker(ticker)
        info = stock.fast_info

        # 2. Проверяем, какие ключи реально доступны
        if "lastPrice" not in info or "previousClose" not in info:

        
            return SensorSignal(
                sensor="stock_sensor",
                status="error",
                timestamp=SensorSignal.now_utc(),
                data=dict(info),
                message="Недостаточно данных от Yahoo Finance"
            )

        # 3. Достаём цены
        last_price = info["lastPrice"]
        prev_close = info["previousClose"]

        # 4. Считаем процент изменения
        change_percent = round(
            ((last_price - prev_close) / prev_close) * 100,
            2
        )

        # 5. Определяем статус
        if abs(change_percent) >= 5:
            status = "warning"
            message = f"Сильное движение {ticker}: {change_percent}%"
        else:
            status = "ok"
            message = f"Рынок стабилен ({change_percent}%)"

        # 6. Возвращаем сигнал
        return SensorSignal(
            sensor="stock_sensor",
            status=status,
            timestamp=SensorSignal.now_utc(),
            data={
                "ticker": ticker,
                "price": last_price,
                "previous_close": prev_close,
                "change_percent": change_percent
            },
            message=message
        )

    except Exception as e:
        # 7. Любая ошибка — это сигнал, а не крэш
        return SensorSignal(
            sensor="stock_sensor",
            status="error",
            timestamp=SensorSignal.now_utc(),
            data={},
            message=str(e)
        )
