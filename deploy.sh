#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/Users/sergeiiakimov/Documents/Heartbeat"
DOCKER_DIR="$APP_DIR/docker"

echo "=== DEPLOY START ==="

cd "$APP_DIR"

echo "-> git fetch & reset"
git fetch origin
git reset --hard origin/main

echo "-> ensure venv exists"
if [ ! -x "$APP_DIR/.venv/bin/python" ]; then
  echo "ERROR: venv not found at $APP_DIR/.venv"
  exit 1
fi

echo "-> install/update python deps"
if [ -f "$APP_DIR/requirements.txt" ]; then
  "$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"
else
  echo "requirements.txt not found, skipping pip install"
fi

echo "-> restart heartbeat exporter (launchd)"
launchctl kickstart -k "gui/$(id -u)/com.sergeiiakimov.heartbeat-exporter" || echo "Exporter restart skipped (LaunchAgent not loaded?)"

echo "-> reload Prometheus"
curl -sf -X POST http://localhost:9090/-/reload || echo "Prometheus reload skipped"

echo "-> restart Alertmanager"
if [ -d "$DOCKER_DIR" ]; then
  cd "$DOCKER_DIR"
  docker compose restart alertmanager || echo "Alertmanager restart skipped"
else
  echo "Docker dir not found, skipping Alertmanager"
fi

echo "=== DEPLOY DONE ==="
