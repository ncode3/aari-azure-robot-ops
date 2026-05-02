from __future__ import annotations

import json
import subprocess
from pathlib import Path

import psutil


def _read_text(path: str) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8").strip()
    except OSError:
        return None


def get_cpu_temperature_celsius() -> float | None:
    thermal_value = _read_text("/sys/class/thermal/thermal_zone0/temp")
    if thermal_value:
        try:
            return round(int(thermal_value) / 1000.0, 2)
        except ValueError:
            pass

    try:
        result = subprocess.run(
            ["vcgencmd", "measure_temp"],
            capture_output=True,
            text=True,
            check=False,
        )
        output = result.stdout.strip()
        if output.startswith("temp=") and "'" in output:
            return round(float(output.split("=")[1].split("'")[0]), 2)
    except OSError:
        return None

    return None


def get_uptime_seconds() -> int | None:
    uptime_text = _read_text("/proc/uptime")
    if not uptime_text:
        return None
    try:
        return int(float(uptime_text.split()[0]))
    except (ValueError, IndexError):
        return None


def get_disk_usage() -> dict[str, float | int]:
    usage = psutil.disk_usage("/")
    used_percent = round((usage.used / usage.total) * 100, 2) if usage.total else 0.0
    return {
        "total_bytes": usage.total,
        "used_bytes": usage.used,
        "free_bytes": usage.free,
        "used_percent": used_percent,
    }


def get_wifi_signal_dbm() -> int | None:
    wireless_text = _read_text("/proc/net/wireless")
    if wireless_text:
        lines = [line.strip() for line in wireless_text.splitlines() if ":" in line]
        if lines:
            parts = lines[0].replace(":", " ").split()
            try:
                return int(float(parts[3]))
            except (ValueError, IndexError):
                pass

    try:
        result = subprocess.run(
            ["iwconfig"],
            capture_output=True,
            text=True,
            check=False,
        )
        for line in result.stdout.splitlines():
            if "Signal level=" in line:
                fragment = line.split("Signal level=")[1].split()[0]
                if "dBm" in fragment:
                    return int(fragment.replace("dBm", ""))
    except OSError:
        return None

    return None


def get_wifi_interface() -> str | None:
    wireless_text = _read_text("/proc/net/wireless")
    if not wireless_text:
        return None
    lines = [line.strip() for line in wireless_text.splitlines() if ":" in line]
    if not lines:
        return None
    return lines[0].split(":")[0].strip()


def get_status_snapshot() -> dict[str, object]:
    return {
        "cpu_temperature_celsius": get_cpu_temperature_celsius(),
        "uptime_seconds": get_uptime_seconds(),
        "disk_usage": get_disk_usage(),
        "wifi_signal_dbm": get_wifi_signal_dbm(),
        "wifi_interface": get_wifi_interface(),
    }


if __name__ == "__main__":
    print(json.dumps(get_status_snapshot(), indent=2))
