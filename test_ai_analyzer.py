# test_ai_analyzer.py
from aggregator.sensor_aggregator import run_all_sensors
from ai.analyzer import analyze_signals

signals = run_all_sensors()
result = analyze_signals(signals)

print(result)
