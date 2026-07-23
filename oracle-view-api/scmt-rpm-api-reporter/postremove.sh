#!/bin/bash
set -e

echo "INFO: API Reporter RPM postremove"
echo "INFO: RPM argument: ${1:-unknown}"

systemctl daemon-reload || true

exit 0
