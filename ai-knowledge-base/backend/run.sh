#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -x ".venv/bin/python" ]; then
  echo "未找到 .venv/bin/python，请先创建虚拟环境并安装依赖"
  exit 1
fi

exec .venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
