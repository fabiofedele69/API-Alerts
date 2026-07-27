#!/bin/bash
set -e

echo "INFO: API Reporter RPM preremove"
echo "INFO: RPM argument: ${1:-unknown}"

SERVICE_NAME="api-reporter.service"

# RPM passes:
#   $1 = 0  -> complete uninstall
#   $1 >= 1 -> upgrade/replacement
#
# During an upgrade, do not stop or disable the service.
if [ "${1:-0}" -eq 0 ]; then
    echo "INFO: Complete removal detected; stopping and disabling service"

    if systemctl list-unit-files "${SERVICE_NAME}" >/dev/null 2>&1; then
        systemctl stop "${SERVICE_NAME}" || true
        systemctl disable "${SERVICE_NAME}" || true
    fi

    systemctl daemon-reload || true
else
    echo "INFO: Upgrade detected; service will not be stopped or disabled"
fi

exit 0
