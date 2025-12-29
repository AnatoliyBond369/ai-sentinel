# sensors/gcp_sensor.py

import time
import httpx
from core.schema import SensorSignal
from core.config import GCP_LATENCY_WARNING_MS

def run_gcp_sensor(url: str = "https://www.google.com") -> SensorSignal:
    """
    Сенсор доступности внешнего сервиса (HTTP).
    """

    start_time = time.perf_counter()

    try:
        response = httpx.get(url, timeout=5.0)
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        if response.status_code == 200:
            status = "ok" if latency_ms < GCP_LATENCY_WARNING_MS else "warning"
            message = f"Сервис доступен ({latency_ms} ms)"
        else:
            status = "warning"
            message = f"Ответ {response.status_code}"

        return SensorSignal(
            sensor="gcp_sensor",
            status=status,
            timestamp=SensorSignal.now_utc(),
            data={
                "url": url,
                "status_code": response.status_code,
                "latency_ms": latency_ms
            },
            message=message
        )

    except Exception as e:
        return SensorSignal(
            sensor="gcp_sensor",
            status="error",
            timestamp=SensorSignal.now_utc(),
            data={"url": url},
            message=str(e)
        )
