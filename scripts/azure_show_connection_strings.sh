#!/usr/bin/env bash
set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-rg-aari-robot-ops-dev}"
IOT_HUB_NAME="${IOT_HUB_NAME:-iot-aari-robot-ops-dev}"
STORAGE_ACCOUNT_NAME="${STORAGE_ACCOUNT_NAME:-staarialrobotopsdev}"
DEVICE_ID="${DEVICE_ID:-aari-pi-001}"

echo "Device connection string:"
az iot hub device-identity connection-string show \
  --hub-name "${IOT_HUB_NAME}" \
  --device-id "${DEVICE_ID}" \
  --resource-group "${RESOURCE_GROUP}" \
  --query connectionString \
  --output tsv

echo
echo "Storage connection string:"
az storage account show-connection-string \
  --name "${STORAGE_ACCOUNT_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --query connectionString \
  --output tsv
