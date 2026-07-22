#!/bin/bash

set -euo pipefail

APP_NAME="api-reporter"
SERVICE_NAME="${APP_NAME}.service"

APP_HOME="/app/M50/m50-api-reporter"
APP_USER="um501001"
APP_GROUP="gm501001"

PYTHON_BIN="/app/M50/python-3.10.15/bin/python3"
SYSTEMD_DIR="/etc/systemd/system"

# The installation script is located under <extracted-package>/bin.
PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SOURCE_APP="${PACKAGE_ROOT}/app"
SOURCE_BIN="${PACKAGE_ROOT}/bin"
SOURCE_REQUIREMENTS="${PACKAGE_ROOT}/requirements.txt"
SOURCE_SERVICE="${PACKAGE_ROOT}/services/${SERVICE_NAME}"

echo "Installing ${APP_NAME}"
echo "Package root: ${PACKAGE_ROOT}"
echo "Application target: ${APP_HOME}"

if [[ "${EUID}" -ne 0 ]]; then
    echo "ERROR: This installation script must run as root." >&2
    exit 1
fi

if [[ ! -x "${PYTHON_BIN}" ]]; then
    echo "ERROR: Python executable not found or not executable: ${PYTHON_BIN}" >&2
    exit 1
fi

for required_path in \
    "${SOURCE_APP}" \
    "${SOURCE_BIN}" \
    "${SOURCE_REQUIREMENTS}" \
    "${SOURCE_SERVICE}"
do
    if [[ ! -e "${required_path}" ]]; then
        echo "ERROR: Required deployment file is missing: ${required_path}" >&2
        exit 1
    fi
done

if ! id "${APP_USER}" >/dev/null 2>&1; then
    echo "ERROR: Application user does not exist: ${APP_USER}" >&2
    exit 1
fi

if ! getent group "${APP_GROUP}" >/dev/null 2>&1; then
    echo "ERROR: Application group does not exist: ${APP_GROUP}" >&2
    exit 1
fi

echo "Stopping existing service when present..."

if systemctl list-unit-files "${SERVICE_NAME}" >/dev/null 2>&1; then
    systemctl stop "${SERVICE_NAME}" || true
fi

echo "Creating application directories..."

install -d -m 0755 -o "${APP_USER}" -g "${APP_GROUP}" "${APP_HOME}"
install -d -m 0755 -o "${APP_USER}" -g "${APP_GROUP}" "${APP_HOME}/logs"
install -d -m 0755 -o "${APP_USER}" -g "${APP_GROUP}" "${APP_HOME}/config"

echo "Installing application source..."

rm -rf "${APP_HOME}/app"
mkdir -p "${APP_HOME}/app"
cp -a "${SOURCE_APP}/." "${APP_HOME}/app/"

echo "Installing runtime scripts..."

rm -rf "${APP_HOME}/bin"
mkdir -p "${APP_HOME}/bin"
cp -a "${SOURCE_BIN}/." "${APP_HOME}/bin/"

# The installer itself is not needed in the runtime bin directory.
rm -f "${APP_HOME}/bin/install-api-reporter.sh"

chmod 0755 "${APP_HOME}/bin/start-api-reporter.sh"

echo "Installing Python requirements..."

install -m 0644 \
    "${SOURCE_REQUIREMENTS}" \
    "${APP_HOME}/requirements.txt"

if [[ ! -x "${APP_HOME}/venv/bin/python" ]]; then
    echo "Creating Python virtual environment..."

    rm -rf "${APP_HOME}/venv"
    "${PYTHON_BIN}" -m venv "${APP_HOME}/venv"
else
    echo "Existing Python virtual environment found."
fi

echo "Installing Python dependencies..."

"${APP_HOME}/venv/bin/python" -m pip install \
    --disable-pip-version-check \
    -r "${APP_HOME}/requirements.txt"

echo "Installing systemd service..."

install -m 0644 \
    "${SOURCE_SERVICE}" \
    "${SYSTEMD_DIR}/${SERVICE_NAME}"

echo "Applying ownership and permissions..."

chown -R "${APP_USER}:${APP_GROUP}" "${APP_HOME}"

find "${APP_HOME}/app" -type d -exec chmod 0755 {} \;
find "${APP_HOME}/app" -type f -exec chmod 0644 {} \;

chmod 0755 "${APP_HOME}/bin/start-api-reporter.sh"

echo "Reloading systemd and starting service..."

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

echo "Checking service status..."

if ! systemctl is-active --quiet "${SERVICE_NAME}"; then
    echo "ERROR: ${SERVICE_NAME} did not start successfully." >&2
    systemctl status "${SERVICE_NAME}" --no-pager || true
    journalctl -u "${SERVICE_NAME}" -n 100 --no-pager || true
    exit 1
fi

echo "${APP_NAME} installed and started successfully."
systemctl status "${SERVICE_NAME}" --no-pager
