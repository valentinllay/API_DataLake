#!/bin/bash
set -euo pipefail

APP_DIR="/home/ubuntu/API_DataLake"
if [[ -d "$APP_DIR" ]]; then
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] Removing old application directory $APP_DIR"
    rm -rf "$APP_DIR"
else
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] No existing directory to remove"
fi