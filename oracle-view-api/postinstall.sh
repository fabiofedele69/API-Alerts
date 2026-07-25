#!/bin/bash
set -e

echo "INFO: API Reporter RPM postinstall"
echo "INFO: RPM argument: ${1:-unknown}"

APP_HOME="/app/M50/m50-api-reporter"
APP_USER="um501001"
APP_GROUP="gm501001"

SERVICE_NAME="api-reporter.service"
SERVICE_SOURCE="${APP_HOME}/services/${SERVICE_NAME}"
SERVICE_TARGET="/etc/systemd/system/${SERVICE_NAME}"

START_SCRIPT="${APP_HOME}/bin/start-api-reporter.sh"
INSTALL_SCRIPT="${APP_HOME}/bin/install-api-reporter.sh"

echo "INFO: Validating packaged files"

if [[ ! -f "${SERVICE_SOURCE}" ]]; then
    echo "ERROR: Service file not found: ${SERVICE_SOURCE}" >&2
    exit 1
fi

if [[ ! -f "${START_SCRIPT}" ]]; then
    echo "ERROR: Start script not found: ${START_SCRIPT}" >&2
    exit 1
fi

if [[ ! -f "${INSTALL_SCRIPT}" ]]; then
    echo "ERROR: Install script not found: ${INSTALL_SCRIPT}" >&2
    exit 1
fi

echo "INFO: Setting script permissions"

chmod 0755 "${START_SCRIPT}"
chmod 0755 "${INSTALL_SCRIPT}"

echo "INFO: Installing systemd service"

install -m 0644 \
    "${SERVICE_SOURCE}" \
    "${SERVICE_TARGET}"

echo "INFO: Setting application ownership"

chown -R "${APP_USER}:${APP_GROUP}" "${APP_HOME}"

echo "INFO: Reloading systemd configuration"

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"

echo "INFO: API Reporter RPM postinstall completed successfully"

exit 0
