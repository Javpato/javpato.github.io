#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
.venv/bin/pip install -r cv/requirements.txt
mkdir -p build/tools
curl -fL --retry 3 -o build/tools/tectonic.tar.gz https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.17.0/tectonic-0.17.0-x86_64-unknown-linux-musl.tar.gz
python3 - <<'PY'
import hashlib,pathlib
assert hashlib.sha256(pathlib.Path('build/tools/tectonic.tar.gz').read_bytes()).hexdigest()=='8533d07f9ccbd7a65824b9e0459041bca34af1eb33daba48f59215593753a3b7'
PY
tar -xzf build/tools/tectonic.tar.gz -C build/tools
printf '%s\n' 'Ready. Run: TECTONIC=build/tools/tectonic .venv/bin/python scripts/cv.py build'
