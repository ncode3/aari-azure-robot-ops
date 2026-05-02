from __future__ import annotations

from datetime import UTC, datetime

from config import Settings
from device_status import get_status_snapshot


def build_telemetry_payload(settings: Settings) -> dict[str, object]:
    status = get_status_snapshot()
    return {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "device_id": settings.robot_id,
        "robot_id": settings.robot_id,
        "heartbeat": True,
        "robot_status": settings.robot_status,
        "cpu_temperature_celsius": status["cpu_temperature_celsius"],
        "uptime_seconds": status["uptime_seconds"],
        "disk_usage": status["disk_usage"],
        "wifi_signal_dbm": status["wifi_signal_dbm"],
        "wifi_interface": status["wifi_interface"],
    }
