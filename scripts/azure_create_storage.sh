#!/usr/bin/env bash
set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-rg-aari-robot-ops-dev}"
LOCATION="${LOCATION:-eastus}"
STORAGE_ACCOUNT_NAME="${STORAGE_ACCOUNT_NAME:-staarialrobotopsdev}"
BLOB_CONTAINER_NAME="${BLOB_CONTAINER_NAME:-robot-incidents}"

echo "Creating storage account: ${STORAGE_ACCOUNT_NAME}"
az storage account create \
  --name "${STORAGE_ACCOUNT_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --location "${LOCATION}" \
  --sku Standard_LRS \
  --kind StorageV2 \
  --allow-blob-public-access false \
  --https-only true

echo "Fetching storage connection string"
STORAGE_CONNECTION_STRING="$(az storage account show-connection-string \
  --name "${STORAGE_ACCOUNT_NAME}" \
  --resource-group "${RESOURCE_GROUP}" \
  --query connectionString \
  --output tsv)"

echo "Creating blob container: ${BLOB_CONTAINER_NAME}"
az storage container create \
  --name "${BLOB_CONTAINER_NAME}" \
  --connection-string "${STORAGE_CONNECTION_STRING}" \
  --public-access off

echo
echo "Azure storage resources created."
echo "RESOURCE_GROUP=${RESOURCE_GROUP}"
echo "STORAGE_ACCOUNT_NAME=${STORAGE_ACCOUNT_NAME}"
echo "BLOB_CONTAINER_NAME=${BLOB_CONTAINER_NAME}"
