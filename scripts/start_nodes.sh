#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-${ROOT_DIR}/.venv/bin/python}"
HOST="${KNOWMESH_HOST:-127.0.0.1}"
BASE_PORT="${KNOWMESH_BASE_PORT:-8001}"
APP_IMPORT="${KNOWMESH_APP_IMPORT:-knowmesh_api.main:app}"
LOG_DIR="${KNOWMESH_LOG_DIR:-${ROOT_DIR}/logs/nodes}"
PID_DIR="${KNOWMESH_PID_DIR:-${ROOT_DIR}/.run/nodes}"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  PYTHON_BIN="$(command -v python3 || true)"
fi
if [[ -z "${PYTHON_BIN}" ]] || ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "ERROR: Python executable not found. Run scripts/setup.sh first." >&2
  exit 1
fi

API_SRC="${ROOT_DIR}/apps/api/src"
if [[ ! -d "${API_SRC}/knowmesh_api" ]]; then
  echo "ERROR: API package not found at ${API_SRC}/knowmesh_api." >&2
  exit 1
fi

mkdir -p "${LOG_DIR}" "${PID_DIR}"
export PYTHONPATH="${API_SRC}${PYTHONPATH:+:${PYTHONPATH}}"

started=()
cleanup() {
  local pid
  for pid in "${started[@]}"; do
    kill "${pid}" 2>/dev/null || true
  done
}
trap cleanup INT TERM

for node in a b c; do
  port=$((BASE_PORT + $(printf '%d' "'${node}") - 97))
  pid_file="${PID_DIR}/node-${node}.pid"
  log_file="${LOG_DIR}/node-${node}.log"

  if [[ -f "${pid_file}" ]]; then
    old_pid="$(cat "${pid_file}" 2>/dev/null || true)"
    if [[ -n "${old_pid}" ]] && kill -0 "${old_pid}" 2>/dev/null; then
      echo "ERROR: node-${node} already appears to be running (PID ${old_pid})." >&2
      exit 1
    fi
    rm -f "${pid_file}"
  fi

  KNOWMESH_NODE_ID="node-${node}" "${PYTHON_BIN}" -m uvicorn "${APP_IMPORT}" \
    --host "${HOST}" --port "${port}" >>"${log_file}" 2>&1 &
  pid=$!
  echo "${pid}" > "${pid_file}"
  started+=("${pid}")
  echo "Started node-${node}: http://${HOST}:${port} (PID ${pid})"
done

echo "Logs: ${LOG_DIR}"
echo "Press Ctrl+C to stop processes started by this script."
wait
