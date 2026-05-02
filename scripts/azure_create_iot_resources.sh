#!/usr/bin/env bash
set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-rg-aari-robot-ops-dev}"
LOCATION="${LOCATION:-eastus}"
IOT_HUB_NAME="${IOT_HUB_NAME:-iot-aari-robot-ops-dev}"
IOT_HUB_SKU="${IOT_HUB_SKU:-S1}"

echo "Creating resource group: ${RESOURCE_GROUP}"
az group create \
  --name "${RESOURCE_GROUP}" \
  --location "${LOCATION}"

echo "Creating IoT Hub: ${IOT_HUB_NAME}"
az iot hub create \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${IOT_HUB_NAME}" \
  --location "${LOCATION}" \
  --sku "${IOT_HUB_SKU}" \
  --partition-count 2

echo
echo "Azure IoT resources created."
echo "RESOURCE_GROUP=${RESOURCE_GROUP}"
echo "IOT_HUB_NAME=${IOT_HUB_NAME}"
