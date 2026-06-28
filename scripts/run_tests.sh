#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
pytest tests/ -v --cov=app --cov-report=term-missing --cov-fail-under=85 "$@"
