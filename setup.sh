#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$PROJECT_ROOT/.venv"
PYTHON_PATH="$VENV_PATH/bin/python"
SKIP_RUN=0

for argument in "$@"; do
    case "$argument" in
        --skip-run)
            SKIP_RUN=1
            ;;
        *)
            echo "Uso: $0 [--skip-run]" >&2
            exit 2
            ;;
    esac
done

if command -v python3 >/dev/null 2>&1; then
    SYSTEM_PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
    SYSTEM_PYTHON="$(command -v python)"
else
    echo "Python 3 nao foi encontrado no PATH. Instale Python 3.11+ e tente novamente." >&2
    exit 1
fi

if [[ ! -x "$PYTHON_PATH" ]]; then
    "$SYSTEM_PYTHON" -m venv "$VENV_PATH"
fi

"$PYTHON_PATH" -m pip install --upgrade pip
"$PYTHON_PATH" -m pip install -r "$PROJECT_ROOT/requirements.txt"

if [[ "$SKIP_RUN" -eq 0 ]]; then
    exec "$PYTHON_PATH" "$PROJECT_ROOT/main.py"
fi
