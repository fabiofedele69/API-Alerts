#!/bin/bash
set -euo pipefail

echo "INFO: API Reporter RPM postinstall"
echo "INFO: RPM argument: ${1:-unknown}"

APP_HOME="/app/M50/m50-api-reporter"
APP_USER="um501001"
APP_GROUP="gm501001"

PYTHON_BIN="/app/M50/m50-python-3.10.15/bin/python3"

SERVICE_NAME="api-reporter.service"
SOURCE_SERVICE="${APP_HOME}/services/${SERVICE_NAME}"
SYSTEMD_DIR="/etc/systemd/system"

CA_BUNDLE="${CA_BUNDLE:-/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem}"
PYPI_INDEX_URL="${PYPI_INDEX_URL:-https://it4it-nexus-tp-repo.swissbank.com/repository/public-lib-python-pypi/simple}"

echo "INFO: Validating installation prerequisites"

if ! id "${APP_USER}" >/dev/null 2>&1; then
    echo "ERROR: Application user does not exist: ${APP_USER}" >&2
    exit 1
fi

if ! getent group "${APP_GROUP}" >/dev/null 2>&1; then
    echo "ERROR: Application group does not exist: ${APP_GROUP}" >&2
    exit 1
fi

if [[ ! -x "${PYTHON_BIN}" ]]; then
    echo "ERROR: Python executable not found or not executable: ${PYTHON_BIN}" >&2
    exit 1
fi

for required_file in \
    "${APP_HOME}/requirements.txt" \
    "${APP_HOME}/bin/start-api-reporter.sh" \
    "${SOURCE_SERVICE}"
do
    if [[ ! -f "${required_file}" ]]; then
        echo "ERROR: Required RPM file is missing: ${required_file}" >&2
        exit 1
    fi
done

if [[ ! -f "${CA_BUNDLE}" ]]; then
    echo "ERROR: CA bundle not found: ${CA_BUNDLE}" >&2
    exit 1
fi

echo "INFO: Creating runtime directories"

install -d \
    -m 0755 \
    -o "${APP_USER}" \
    -g "${APP_GROUP}" \
    "${APP_HOME}/logs"

install -d \
    -m 0755 \
    -o "${APP_USER}" \
    -g "${APP_GROUP}" \
    "${APP_HOME}/config"

echo "INFO: Creating Python virtual environment"

if [[ ! -d "${APP_HOME}/venv" ]]; then
    "${PYTHON_BIN}" -m venv "${APP_HOME}/venv"
else
    echo "INFO: Existing Python virtual environment found"
fi

echo "INFO: Installing/updating Python dependencies"

"${APP_HOME}/venv/bin/python" -m pip install \
    --disable-pip-version-check \
    --upgrade \
    --cert "${CA_BUNDLE}" \
    --index-url "${PYPI_INDEX_URL}" \
    -r "${APP_HOME}/requirements.txt"

echo "INFO: Installing systemd service"

install -m 0644 \
    "${SOURCE_SERVICE}" \
    "${SYSTEMD_DIR}/${SERVICE_NAME}"

echo "INFO: Applying ownership and permissions"

chown -R "${APP_USER}:${APP_GROUP}" "${APP_HOME}"

find "${APP_HOME}/app" \
    -type d \
    -exec chmod 0755 {} \;

find "${APP_HOME}/app" \
    -type f \
    -exec chmod 0644 {} \;

find "${APP_HOME}/bin" \
    -type f \
    -exec chmod 0755 {} \;

echo "INFO: Reloading systemd and starting service"

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

echo "INFO: Checking service status"

if ! systemctl is-active --quiet "${SERVICE_NAME}"; then
    echo "ERROR: ${SERVICE_NAME} did not start successfully" >&2
    systemctl status "${SERVICE_NAME}" --no-pager || true
    journalctl -u "${SERVICE_NAME}" -n 100 --no-pager || true
    exit 1
fi

echo "INFO: API Reporter RPM postinstall completed successfully"
systemctl status "${SERVICE_NAME}" --no-pager

exit 0
