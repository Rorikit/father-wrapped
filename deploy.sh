#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/father-wrapped}"
REPO_URL="${REPO_URL:-https://github.com/Rorikit/father-wrapped.git}"
PYTHON_BIN="${PYTHON_BIN:-python3.11}"

if [ ! -d "$APP_DIR/.git" ]; then
  git clone "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"
git pull --ff-only

"$PYTHON_BIN" -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q

echo "Deploy files are ready in $APP_DIR"
echo "For SpaceWeb mod_wsgi, set the domain document root to this directory and use wsgi.py as the WSGI entry point."
