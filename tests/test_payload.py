from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from config import Settings
from telemetry import build_telemetry_payload


def test_payload_contains_expected_fields() -> None:
    settings = Settings(
        simulate_only=False,
        iothub_device_connection_string="HostName=test;DeviceId=test;SharedAccessKey=test",
        blob_storage_connection_string=None,
        blob_container_name="robot-incidents",
        log_level="INFO",
        telemetry_interval_seconds=60,
        robot_id="aari-pi-001",
        robot_status="idle",
        device_timezone="UTC",
    )

    payload = build_telemetry_payload(settings)

    assert payload["heartbeat"] is True
    assert payload["device_id"] == "aari-pi-001"
    assert payload["robot_id"] == "aari-pi-001"
    assert payload["robot_status"] == "idle"
    assert "timestamp_utc" in payload
    assert "cpu_temperature_celsius" in payload
    assert "uptime_seconds" in payload
    assert "disk_usage" in payload
    assert "wifi_signal_dbm" in payload
