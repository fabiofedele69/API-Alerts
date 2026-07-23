APP_NAME="api-reporter"
APP_HOME="/app/M50/m50-api-reporter"

PYTHON_BIN="/app/M50/m50-python-3.10.15/bin/python3"

...

echo "Installing application source..."

echo "Installing runtime scripts..."

echo "Installing Python requirements..."

echo "Installing/updating Python dependencies..."

PYPI_INDEX_URL="https://it4it-nexus-tp-repo.swissbank.com/repository/public-lib-python-pypi/simple"

...

systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl restart ${SERVICE_NAME}
