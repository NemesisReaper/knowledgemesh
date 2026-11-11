#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/.venv}"
REQUIREMENTS_FILE="${REQUIREMENTS_FILE:-${ROOT_DIR}/requirements.txt}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "ERROR: ${PYTHON_BIN} was not found. Install Python 3.10+ first." >&2
  exit 1
fi

"${PYTHON_BIN}" - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise SystemExit("ERROR: KnowMesh scripts require Python 3.10 or newer.")
print(f"Using Python {sys.version.split()[0]}")
PY

if [[ ! -f "${REQUIREMENTS_FILE}" ]]; then
  echo "ERROR: requirements file not found: ${REQUIREMENTS_FILE}" >&2
  exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

if [[ -x "${VENV_DIR}/bin/python" ]]; then
  VENV_PY="${VENV_DIR}/bin/python"
  VENV_PIP="${VENV_DIR}/bin/pip"
elif [[ -x "${VENV_DIR}/Scripts/python.exe" ]]; then
  VENV_PY="${VENV_DIR}/Scripts/python.exe"
  VENV_PIP="${VENV_DIR}/Scripts/pip.exe"
else
  echo "ERROR: could not locate Python in virtual environment: ${VENV_DIR}" >&2
  exit 1
fi

"${VENV_PY}" -m pip install --upgrade pip
"${VENV_PIP}" install -r "${REQUIREMENTS_FILE}"

echo
echo "KnowMesh Python dependencies installed."
echo "Activate with:"
if [[ -f "${VENV_DIR}/bin/activate" ]]; then
  echo "  source \"${VENV_DIR}/bin/activate\""
else
  echo "  ${VENV_DIR}\\Scripts\\activate"
fi
