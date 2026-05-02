# Azure Setup

## Preconditions

The scripts do not log in for you. Run these manually first:

```bash
az login
az account set --subscription "<YOUR_SUBSCRIPTION_ID>"
az extension add --upgrade -n azure-iot
```

## Default Shell Variables

These scripts support overrides through environment variables:

```bash
export RESOURCE_GROUP="rg-aari-robot-ops-dev"
export LOCATION="eastus"
export IOT_HUB_NAME="iot-aari-robot-ops-dev"
export IOT_HUB_SKU="S1"
export STORAGE_ACCOUNT_NAME="staarialrobotopsdev"
export BLOB_CONTAINER_NAME="robot-incidents"
export DEVICE_ID="aari-pi-001"
```

## Create IoT Resources

```bash
bash scripts/azure_create_iot_resources.sh
```

This creates:

- resource group
- IoT Hub

## Register The Device

```bash
bash scripts/azure_register_device.sh
```

This creates one device identity and prints the device connection string.

## Create Storage

```bash
bash scripts/azure_create_storage.sh
```

This creates:

- storage account
- blob container

Public blob access is disabled.

## Show Connection Strings

```bash
bash scripts/azure_show_connection_strings.sh
```

Copy the values you need into `.env`.

Do not commit `.env`.
