#!/bin/bash
set -e

echo "INFO: API Reporter RPM preremove"
echo "INFO: RPM argument: ${1:-unknown}"

SERVICE_NAME="api-reporter.service"

if systemctl list-unit-files "${SERVICE_NAME}" >/dev/null 2>&1; then
    systemctl stop "${SERVICE_NAME}" || true
    systemctl disable "${SERVICE_NAME}" || true
fi

systemctl daemon-reload || true

exit 0
