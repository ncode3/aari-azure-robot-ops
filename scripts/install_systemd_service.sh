#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_SOURCE="${REPO_ROOT}/systemd/aari-robot-agent.service"
SERVICE_DEST="/etc/systemd/system/aari-robot-agent.service"
SERVICE_USER="${SUDO_USER:-${USER}}"

if [[ ! -f "${SERVICE_SOURCE}" ]]; then
  echo "Missing service file: ${SERVICE_SOURCE}" >&2
  exit 1
fi

sed \
  -e "s|__AARI_REPO_ROOT__|${REPO_ROOT}|g" \
  -e "s|__AARI_USER__|${SERVICE_USER}|g" \
  "${SERVICE_SOURCE}" > "${SERVICE_DEST}"
chmod 0644 "${SERVICE_DEST}"
systemctl daemon-reload

echo "Installed ${SERVICE_DEST}"
echo "Next commands:"
echo "  sudo systemctl enable aari-robot-agent"
echo "  sudo systemctl start aari-robot-agent"
echo "  sudo systemctl status aari-robot-agent"
