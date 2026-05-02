from __future__ import annotations

import argparse
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

from azure.storage.blob import BlobClient

from config import get_settings


def _utc_parts() -> tuple[str, str]:
    now = datetime.now(UTC)
    return now.strftime("%Y-%m-%d"), now.strftime("%Y%m%dT%H%M%SZ")


def build_blob_name(file_path: Path, device_id: str) -> str:
    day, timestamp = _utc_parts()
    suffix = file_path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        folder = "snapshots"
        extension = ".jpg"
    else:
        folder = "incidents"
        extension = suffix or ".json"
    return f"{folder}/{device_id}/{day}/{timestamp}{extension}"


def upload_file(file_path: str, container_name: str | None = None) -> str:
    settings = get_settings()
    if not settings.blob_storage_connection_string:
        raise ValueError("BLOB_STORAGE_CONNECTION_STRING is required for uploads.")

    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    resolved_container = container_name or settings.blob_container_name
    blob_name = build_blob_name(path, settings.robot_id)
    client = BlobClient.from_connection_string(
        conn_str=settings.blob_storage_connection_string,
        container_name=resolved_container,
        blob_name=blob_name,
    )

    with path.open("rb") as handle:
        client.upload_blob(handle, overwrite=True)

    return client.url


def upload_event_json(payload: dict[str, object], output_path: str | None = None) -> str:
    settings = get_settings()
    _, timestamp = _utc_parts()
    event_path = Path(output_path) if output_path else Path("logs") / f"event-{timestamp}.json"
    event_path.parent.mkdir(parents=True, exist_ok=True)
    event_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return upload_file(str(event_path), settings.blob_container_name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload a local file to Azure Blob Storage.")
    parser.add_argument("file_path", help="Path to the file to upload")
    parser.add_argument(
        "--container",
        default=None,
        help="Blob container name. Defaults to BLOB_CONTAINER_NAME from .env.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    blob_url = upload_file(args.file_path, args.container)
    logging.info("Uploaded file to %s", blob_url)


if __name__ == "__main__":
    main()
