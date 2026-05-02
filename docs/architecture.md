# Architecture

## Purpose

`aari-azure-robot-ops` is a one-device-first robot gateway for Raspberry Pi OS. The Pi collects local system health, sends telemetry to Azure IoT Hub, and can optionally upload incident files to Azure Blob Storage.

## Core Components

### Raspberry Pi Agent

The Python agent:

- reads `.env`
- gathers device health
- builds a JSON payload
- sends telemetry to Azure IoT Hub
- retries on failure
- logs to `./logs/robot-agent.log`
- shuts down cleanly on interrupt or service stop

### Azure IoT Hub

The IoT Hub is the ingestion point for device telemetry. Each Pi has its own device identity and connection string.

### Azure Blob Storage

Blob Storage is optional and is used for uploads such as:

- incident JSON
- log bundles
- captured snapshots

## Data Flow

1. Pi starts the agent
2. Agent loads `.env`
3. Agent collects CPU temperature, uptime, disk usage, and Wi-Fi signal when available
4. Agent sends JSON telemetry to IoT Hub
5. Agent writes local logs
6. Optional upload scripts send event or image files to Blob Storage

## Blob Path Design

Uploads are grouped by type, device, and date:

- `incidents/<device_id>/<yyyy-mm-dd>/<timestamp>.json`
- `snapshots/<device_id>/<yyyy-mm-dd>/<timestamp>.jpg`

## Design Constraints

- no automatic deployment
- no committed secrets
- no requirement for camera hardware
- no requirement for Docker or Kubernetes
- no OTA in the MVP

## Why This Shape Works

This repo gives you the minimum viable operational path:

- one Pi
- one agent
- one identity
- one telemetry path
- one optional storage path

That is enough to validate hardware, networking, Azure connectivity, and service reliability before adding more complexity.
