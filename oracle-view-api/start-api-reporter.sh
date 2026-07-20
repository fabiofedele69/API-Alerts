set -euo pipefail

export LD_LIBRARY_PATH=/app/M50/m50-openssl-1.1.1w/lib:/opt/CA/SharedComponents/Csam/SockAdapter/lib:/opt/CA/SharedComponents/Csam/SockAdapter/lib64:${LD_LIBRARY_PATH:-}

...

cd "$APP_HOME"

echo "APP_ENV=$APP_ENV"
echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH"

exec "$APP_HOME/venv/bin/python" \
    -m uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 8000


sudo -u um501001 bash -c 'export LD_LIBRARY_PATH=/app/M50/m50-openssl-1.1.1w/lib:${LD_LIBRARY_PATH:-} /app/M50/m50-api-reporter/venv/bin/python -c "import ssl; print(ssl.OPENSSL_VERSION)"'
