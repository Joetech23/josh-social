#!/usr/bin/env bash
# Render a 3D brand object to a transparent PNG.
#   design/3d/render-3d.sh <asset> [size]      assets: eagle | coin | bubble | lock
# Output: design/3d/out/<asset>.png. First run installs three.js with npm.
set -euo pipefail
cd "$(dirname "$0")"
asset="${1:?usage: render-3d.sh <eagle|coin|bubble|lock> [size]}"; size="${2:-1200}"
[ -d node_modules/three ] || npm install --silent
browser="${ES_BROWSER:-$(command -v chrome-headless-shell || ls /opt/pw-browsers/chromium_headless_shell-*/*/headless_shell 2>/dev/null | tail -1 || command -v chromium)}"
port="$(python3 -c "import socket; s=socket.socket(); s.bind(('127.0.0.1',0)); print(s.getsockname()[1])")"
python3 -m http.server "$port" --bind 127.0.0.1 >/dev/null 2>&1 & srv=$!
trap 'kill $srv' EXIT
sleep 1
mkdir -p out
"$browser" --headless --no-sandbox --use-angle=swiftshader --enable-unsafe-swiftshader --hide-scrollbars \
  --default-background-color=00000000 --virtual-time-budget=15000 --window-size="$size,$size" \
  --screenshot="$PWD/out/$asset.png" "http://127.0.0.1:$port/render.html?asset=$asset&w=$size&h=$size" >/dev/null 2>&1
echo "design/3d/out/$asset.png"
