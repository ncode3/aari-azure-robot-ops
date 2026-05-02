# Hardware Setup

## Supported MVP Hardware

This repo assumes a Raspberry Pi 3-class device or similar with:

- microSD boot storage
- Wi-Fi or Ethernet
- micro-USB power
- optional CSI camera connector
- optional GPIO header usage later

The current MVP does not require motors, GPIO sensors, or camera hardware.

## Human-Owned Physical Steps

The human handles:

- flashing Raspberry Pi OS
- inserting the microSD card
- connecting Wi-Fi or Ethernet
- connecting power
- enabling the camera if a camera is installed

## Raspberry Pi OS Preparation

Run on the Pi:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git
```

If you plan to capture snapshots, install camera tooling:

```bash
sudo apt install -y libcamera-apps
```

## Clone The Repo

```bash
git clone <repo-url>
cd aari-azure-robot-ops
```

## Prepare Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Camera Notes

Camera support is optional.

If a camera is connected and enabled, you can test:

```bash
python3 src/camera_snapshot.py
```

If the camera is missing, the repo still works. The main telemetry agent does not depend on camera hardware.
