from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / ".env"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "robot-agent.log"

load_dotenv(ENV_PATH)


@dataclass(frozen=True)
class Settings:
    simulate_only: bool
    iothub_device_connection_string: str
    blob_storage_connection_string: str | None
    blob_container_name: str
    log_level: str
    telemetry_interval_seconds: int
    robot_id: str
    robot_status: str
    device_timezone: str


def get_settings() -> Settings:
    return Settings(
        simulate_only=os.getenv("SIMULATE_ONLY", "false").strip().lower() in {"1", "true", "yes", "on"},
        iothub_device_connection_string=os.getenv("IOTHUB_DEVICE_CONNECTION_STRING", "").strip(),
        blob_storage_connection_string=os.getenv("BLOB_STORAGE_CONNECTION_STRING", "").strip() or None,
        blob_container_name=os.getenv("BLOB_CONTAINER_NAME", "robot-incidents").strip(),
        log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
        telemetry_interval_seconds=max(5, int(os.getenv("TELEMETRY_INTERVAL_SECONDS", "60"))),
        robot_id=os.getenv("ROBOT_ID", "aari-pi-001").strip(),
        robot_status=os.getenv("ROBOT_STATUS", "idle").strip(),
        device_timezone=os.getenv("DEVICE_TIMEZONE", "UTC").strip(),
    )


def validate_settings(settings: Settings) -> None:
    if not settings.simulate_only and not settings.iothub_device_connection_string:
        raise ValueError("IOTHUB_DEVICE_CONNECTION_STRING is required in .env")


def ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
