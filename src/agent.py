from __future__ import annotations

import json
import logging
import signal
import time
from logging.handlers import RotatingFileHandler

from azure.iot.device import IoTHubDeviceClient, Message

from config import LOG_FILE, ensure_log_dir, get_settings, validate_settings
from telemetry import build_telemetry_payload


SHOULD_STOP = False


def configure_logging(level: str) -> None:
    ensure_log_dir()
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=3)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)


def create_client(connection_string: str) -> IoTHubDeviceClient:
    client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    client.connect()
    return client


def _request_shutdown(signum: int, _frame: object) -> None:
    global SHOULD_STOP
    SHOULD_STOP = True
    logging.getLogger("robot-agent").info("Received signal %s, shutting down.", signum)


def run_forever() -> None:
    global SHOULD_STOP
    settings = get_settings()
    validate_settings(settings)
    configure_logging(settings.log_level)
    signal.signal(signal.SIGTERM, _request_shutdown)
    signal.signal(signal.SIGINT, _request_shutdown)

    logger = logging.getLogger("robot-agent")
    logger.info("Starting AARI robot agent for robot_id=%s", settings.robot_id)
    if settings.simulate_only:
        logger.info("Running in simulator mode. Telemetry will be logged locally and not sent to Azure IoT Hub.")

    client: IoTHubDeviceClient | None = None
    retry_delay_seconds = 5

    while not SHOULD_STOP:
        try:
            if client is None:
                if settings.simulate_only:
                    retry_delay_seconds = 5
                else:
                    logger.info("Connecting to Azure IoT Hub")
                    client = create_client(settings.iothub_device_connection_string)
                    retry_delay_seconds = 5

            payload = build_telemetry_payload(settings)
            if settings.simulate_only:
                logger.info("Simulated telemetry send: %s", payload)
            else:
                message = Message(json.dumps(payload))
                message.content_encoding = "utf-8"
                message.content_type = "application/json"

                client.send_message(message)
                logger.info("Telemetry sent: %s", payload)
            time.sleep(settings.telemetry_interval_seconds)

        except KeyboardInterrupt:
            logger.info("Agent interrupted by user, shutting down.")
            break
        except Exception as exc:
            logger.exception("Telemetry loop error: %s", exc)
            if client is not None:
                try:
                    client.shutdown()
                except Exception:
                    logger.debug("Client shutdown after error failed", exc_info=True)
                client = None

            logger.info("Retrying in %s seconds", retry_delay_seconds)
            time.sleep(retry_delay_seconds)
            retry_delay_seconds = min(retry_delay_seconds * 2, 60)

    if client is not None:
        try:
            client.shutdown()
        except Exception:
            logger.debug("Final client shutdown failed", exc_info=True)


if __name__ == "__main__":
    run_forever()
