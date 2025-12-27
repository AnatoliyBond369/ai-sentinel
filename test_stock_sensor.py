# test_stock_sensor.py

from sensors.stock_sensor import run_stock_sensor

signal = run_stock_sensor("AAPL")
print(signal)
