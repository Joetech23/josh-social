#!/usr/bin/env bash
# Render an Eaglescroft social template to PNG or PDF.
#
#   design/render.sh <template.html> [output.png|output.pdf]
#
# Size comes from the template's <meta name="es-size" content="WxH">.
# PNG renders at 2x for crisp uploads. PDF (for LinkedIn carousels) uses the
# template's own @page size, one slide per page.
#
# Fonts: install Sora, Raleway and JetBrains Mono locally for reliable output
# (templates also @import Google Fonts when network is available):
#   mkdir -p ~/.fonts && cd ~/.fonts && GF=https://raw.githubusercontent.com/google/fonts/main
#   curl -sfL "$GF/ofl/sora/Sora%5Bwght%5D.ttf" -o Sora.ttf
#   curl -sfL "$GF/ofl/raleway/Raleway%5Bwght%5D.ttf" -o Raleway.ttf
#   curl -sfL "$GF/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf" -o JetBrainsMono.ttf
#   fc-cache -f
set -euo pipefail

src="${1:?usage: render.sh <template.html> [output.png|output.pdf]}"
out="${2:-${src%.html}.png}"

# Prefer chrome-headless-shell: full Chrome's new headless mode reserves window
# space, which crops screenshots short of --window-size.
browser="${ES_BROWSER:-}"
[ -z "$browser" ] && browser="$(command -v chrome-headless-shell || true)"
[ -z "$browser" ] && browser="$(ls /opt/pw-browsers/chromium_headless_shell-*/*/headless_shell 2>/dev/null | tail -1 || true)"
[ -z "$browser" ] && browser="$(command -v chromium || command -v chromium-browser || command -v google-chrome || true)"
[ -z "$browser" ] && { echo "No Chromium/Chrome found (set ES_BROWSER)" >&2; exit 1; }

size="$(grep -o 'name="es-size" content="[0-9]*x[0-9]*"' "$src" | grep -o '[0-9]*x[0-9]*' || true)"
[ -z "$size" ] && size="1080x1080"
w="${size%x*}"; h="${size#*x}"

url="file://$(cd "$(dirname "$src")" && pwd)/$(basename "$src")"
mkdir -p "$(dirname "$out")"
out_abs="$(cd "$(dirname "$out")" && pwd)/$(basename "$out")"

common=(--headless --no-sandbox --disable-gpu --hide-scrollbars --virtual-time-budget=4000)

case "$out" in
  *.pdf)
    "$browser" "${common[@]}" --no-pdf-header-footer --print-to-pdf="$out_abs" "$url" 2>/dev/null ;;
  *)
    "$browser" "${common[@]}" --window-size="$w,$h" --force-device-scale-factor=2 \
      --screenshot="$out_abs" "$url" 2>/dev/null ;;
esac
echo "$out_abs  (${w}x${h})"
