#!/bin/bash
set -e

APP_HOME="/app/M50/m50-api-reporter"
APP_USER="um501001"
APP_GROUP="gm501001"
SERVICE_NAME="api-reporter.service"
PYTHON_BIN="/app/M50/m50-python-3.10.15/bin/python3"

echo "INFO: API Reporter RPM preinstall, argument: ${1:-unknown}"

if ! id "${APP_USER}" >/dev/null 2>&1; then
    echo "ERROR: Application user does not exist: ${APP_USER}" >&2
    exit 1
fi

if ! getent group "${APP_GROUP}" >/dev/null 2>&1; then
    echo "ERROR: Application group does not exist: ${APP_GROUP}" >&2
    exit 1
fi

if [[ ! -x "${PYTHON_BIN}" ]]; then
    echo "ERROR: Python executable not found: ${PYTHON_BIN}" >&2
    exit 1
fi

# Stop the current service during an upgrade.
# RPM argument 2 means upgrade.
if [[ "${1:-0}" == "2" ]] &&
   systemctl list-unit-files "${SERVICE_NAME}" >/dev/null 2>&1; then
    echo "INFO: Stopping existing API Reporter service for upgrade."
    systemctl stop "${SERVICE_NAME}" || true
fi

install -d -m 0755 -o "${APP_USER}" -g "${APP_GROUP}" "${APP_HOME}"
install -d -m 0755 -o "${APP_USER}" -g "${APP_GROUP}" "${APP_HOME}/logs"
install -d -m 0755 -o "${APP_USER}" -g "${APP_GROUP}" "${APP_HOME}/config"

exit 0
