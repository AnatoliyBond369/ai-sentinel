# test_aggregator.py

from aggregator.sensor_aggregator import run_all_sensors

signals = run_all_sensors()

for signal in signals:
    print(signal)
