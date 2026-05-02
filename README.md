# aari-azure-robot-ops

Raspberry Pi Azure IoT robot gateway starter repo.

This repo is the MVP for one physical Raspberry Pi acting as a robot gateway:

- reads local device health data
- sends JSON telemetry to Azure IoT Hub
- writes local logs to `./logs/robot-agent.log`
- can optionally upload snapshots, log bundles, or event files to Azure Blob Storage
- can run continuously as a `systemd` service on Raspberry Pi OS

Nothing deploys automatically. The human handles Azure login, secret placement in `.env`, physical hardware setup, and validation. This repo owns the agent code, service file, and Azure helper scripts.

## MVP Success Condition

A Raspberry Pi boots, runs the Python agent as a `systemd` service, sends telemetry to Azure IoT Hub, and can optionally upload event files or snapshots to Azure Blob Storage.

## Repo Structure

```text
aari-azure-robot-ops/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── src/
│   ├── agent.py
│   ├── config.py
│   ├── telemetry.py
│   ├── device_status.py
│   ├── storage_upload.py
│   └── camera_snapshot.py
├── scripts/
│   ├── azure_create_iot_resources.sh
│   ├── azure_register_device.sh
│   ├── azure_create_storage.sh
│   ├── azure_show_connection_strings.sh
│   ├── run_agent.sh
│   └── install_systemd_service.sh
├── systemd/
│   └── aari-robot-agent.service
├── docs/
│   ├── architecture.md
│   ├── hardware-setup.md
│   ├── azure-setup.md
│   ├── manual-runbook.md
│   ├── troubleshooting.md
│   └── phase-3-device-update.md
└── tests/
    └── test_payload.py
```

## What The Agent Sends

Each telemetry message includes:

- `heartbeat`
- `cpu_temperature_celsius`
- `uptime_seconds`
- `disk_usage`
- `wifi_signal_dbm` when available
- `wifi_interface` when available
- `device_id`
- `robot_status`
- `timestamp_utc`

Missing sensors are handled gracefully. If Wi-Fi metrics or CPU temperature are unavailable, the payload still sends with `null` for those fields.

## Default Azure Naming

These defaults are only shell defaults. They are not baked into Azure.

- `RESOURCE_GROUP=rg-aari-robot-ops-dev`
- `LOCATION=eastus`
- `IOT_HUB_NAME=iot-aari-robot-ops-dev`
- `IOT_HUB_SKU=S1`
- `STORAGE_ACCOUNT_NAME=staarialrobotopsdev`
- `BLOB_CONTAINER_NAME=robot-incidents`
- `DEVICE_ID=aari-pi-001`

## Dependencies

Python packages used:

- `azure-iot-device`
- `azure-storage-blob`
- `python-dotenv`
- `psutil`

## Quick Start

### 1. Prepare Azure CLI

```bash
az login
az account set --subscription "<YOUR_SUBSCRIPTION_ID>"
az extension add --upgrade -n azure-iot
```

### 2. Create Azure resources

```bash
bash scripts/azure_create_iot_resources.sh
bash scripts/azure_create_storage.sh
```

### 3. Register the Pi device

```bash
bash scripts/azure_register_device.sh
```

### 4. Show connection strings

```bash
bash scripts/azure_show_connection_strings.sh
```

Copy the values you need into `.env`. Do not commit `.env`.

### 5. Set up Python

Mac/Linux or Raspberry Pi OS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### 6. Create `.env`

```bash
cp .env.example .env
```

Set at minimum:

- `IOTHUB_DEVICE_CONNECTION_STRING`
- `ROBOT_ID`
- `ROBOT_STATUS`

If you want uploads enabled, also set:

- `BLOB_STORAGE_CONNECTION_STRING`
- `BLOB_CONTAINER_NAME`

### 7. Run the agent manually

```bash
python3 src/agent.py
```

### 8. Install as a service on the Pi

```bash
sudo bash scripts/install_systemd_service.sh
sudo systemctl enable aari-robot-agent
sudo systemctl start aari-robot-agent
sudo systemctl status aari-robot-agent
```

### 9. Check logs

```bash
tail -f logs/robot-agent.log
journalctl -u aari-robot-agent -f
```

## Local Simulator Mode

If Azure is not ready yet, you can still test the full agent loop without an IoT Hub connection:

```bash
cp .env.example .env
```

Set:

```text
SIMULATE_ONLY=true
```

Then run:

```bash
python3 src/agent.py
```

In simulator mode, the agent builds the live telemetry payload and logs it locally but does not connect to Azure IoT Hub.

## Optional Blob Uploads

Upload a local incident or snapshot file:

```bash
python3 src/storage_upload.py /path/to/file.json
python3 src/storage_upload.py /path/to/image.jpg
```

Blob paths are created automatically:

- `incidents/<device_id>/<yyyy-mm-dd>/<timestamp>.json`
- `snapshots/<device_id>/<yyyy-mm-dd>/<timestamp>.jpg`

## Optional Camera Snapshot

If a Pi camera is present and `libcamera-still` or `raspistill` is installed:

```bash
python3 src/camera_snapshot.py
```

This is optional. The repo does not require a camera to operate.

## systemd Notes

The installer script writes a service file that:

- runs under the current user
- runs from the actual repo directory
- uses the repo virtual environment
- restarts on failure

## What Not To Build Yet

Do not start by adding:

- OTA as part of the MVP
- Azure IoT Edge
- Kubernetes
- Docker
- Digital Twins
- multi-device fleet orchestration
- dashboard theater

Start with one Pi, one agent, one hub, one clean telemetry path.

## More Documentation

- [docs/architecture.md](docs/architecture.md)
- [docs/hardware-setup.md](docs/hardware-setup.md)
- [docs/azure-setup.md](docs/azure-setup.md)
- [docs/manual-runbook.md](docs/manual-runbook.md)
- [docs/troubleshooting.md](docs/troubleshooting.md)
- [docs/phase-3-device-update.md](docs/phase-3-device-update.md)
