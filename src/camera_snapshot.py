from __future__ import annotations

import argparse
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path


def capture_snapshot(output_dir: str = "snapshots") -> Path:
    target_dir = Path(output_dir).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    output_path = target_dir / f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}.jpg"

    libcamera = shutil.which("libcamera-still")
    raspistill = shutil.which("raspistill")

    if libcamera:
        command = [libcamera, "-n", "-o", str(output_path)]
    elif raspistill:
        command = [raspistill, "-n", "-o", str(output_path)]
    else:
        raise RuntimeError(
            "No camera capture command found. Install libcamera-still on Raspberry Pi OS or connect a supported camera."
        )

    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Camera capture failed.")

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture a camera snapshot if camera hardware is present.")
    parser.add_argument("--output-dir", default="snapshots", help="Directory for captured image output.")
    args = parser.parse_args()

    image_path = capture_snapshot(args.output_dir)
    print(image_path)


if __name__ == "__main__":
    main()
