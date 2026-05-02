# Troubleshooting

## `az iot` commands fail

Install the Azure IoT CLI extension:

```bash
az extension add --upgrade -n azure-iot
```

## Device connection string missing

Run:

```bash
bash scripts/azure_register_device.sh
```

Then copy the printed device connection string into `.env`.

## Agent exits with `IOTHUB_DEVICE_CONNECTION_STRING is required`

Either:

- put the real device connection string into `.env`

or:

- set `SIMULATE_ONLY=true` for local dry-run testing

## No Wi-Fi signal appears

That is acceptable.

The Pi may be on Ethernet, or the OS may not expose wireless metrics. Telemetry will still send.

## CPU temperature is `null`

That is acceptable.

Some environments do not expose thermal files or `vcgencmd`. The agent continues running.

## `systemctl` service fails to start

Check:

```bash
sudo systemctl status aari-robot-agent
journalctl -u aari-robot-agent -f
```

Common causes:

- `.env` missing
- `.venv` missing
- dependencies not installed
- repo path moved after service installation

If the repo path changed, rerun:

```bash
sudo bash scripts/install_systemd_service.sh
```

## Blob upload fails

Check:

- `BLOB_STORAGE_CONNECTION_STRING` is present in `.env`
- the target container exists
- the file path exists locally

## Camera snapshot fails

The MVP does not require camera hardware.

If you do want snapshots:

- connect the camera
- enable it in Raspberry Pi OS if needed
- install `libcamera-apps`

If those are absent, `src/camera_snapshot.py` will fail cleanly.
