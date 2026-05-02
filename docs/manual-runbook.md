# Manual Runbook

## Prepare The Environment

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Manual Agent Run

```bash
python3 src/agent.py
```

## Simulator Run

If Azure resources are not ready yet:

1. Set `SIMULATE_ONLY=true` in `.env`
2. Leave `IOTHUB_DEVICE_CONNECTION_STRING` empty
3. Run the agent manually

```bash
python3 src/agent.py
```

## Validate Local Logs

```bash
tail -f logs/robot-agent.log
```

## Validate The systemd Service

```bash
sudo systemctl status aari-robot-agent
journalctl -u aari-robot-agent -f
```

## Install The systemd Service

```bash
sudo bash scripts/install_systemd_service.sh
sudo systemctl enable aari-robot-agent
sudo systemctl start aari-robot-agent
```

## Capture A Snapshot

```bash
python3 src/camera_snapshot.py
```

## Upload An Incident Or Snapshot

```bash
python3 src/storage_upload.py /path/to/file.json
python3 src/storage_upload.py /path/to/file.jpg
```

## Stop The Agent

Manual run:

```bash
Ctrl+C
```

systemd run:

```bash
sudo systemctl stop aari-robot-agent
```
