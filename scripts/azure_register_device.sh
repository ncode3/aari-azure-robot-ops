#!/usr/bin/env bash
set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-rg-aari-robot-ops-dev}"
IOT_HUB_NAME="${IOT_HUB_NAME:-iot-aari-robot-ops-dev}"
DEVICE_ID="${DEVICE_ID:-aari-pi-001}"

echo "Registering device: ${DEVICE_ID}"
az iot hub device-identity create \
  --hub-name "${IOT_HUB_NAME}" \
  --device-id "${DEVICE_ID}" \
  --resource-group "${RESOURCE_GROUP}"

echo
echo "Device connection string:"
az iot hub device-identity connection-string show \
  --hub-name "${IOT_HUB_NAME}" \
  --device-id "${DEVICE_ID}" \
  --resource-group "${RESOURCE_GROUP}" \
  --query connectionString \
  --output tsv
