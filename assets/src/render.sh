#!/usr/bin/env bash
# SVG -> PNG (2x). 캐시된 Playwright Chromium을 헤드리스로 직접 띄운다.
set -e
CHROME="$HOME/.cache/ms-playwright/chromium-1107/chrome-linux/chrome"
DIR="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
for svg in "$DIR"/*.svg; do
  base="$(basename "$svg" .svg)"
  read -r W H < <(python3 - "$svg" <<'PY'
import re,sys
s=open(sys.argv[1]).read(700)
print(re.search(r'width="(\d+)"',s).group(1), re.search(r'height="(\d+)"',s).group(1))
PY
)
  cat > "$TMP/$base.html" <<HTML
<!doctype html><meta charset="utf-8">
<style>html,body{margin:0;padding:0;overflow:hidden}img{display:block;width:${W}px;height:${H}px}</style>
<img src="file://$svg">
HTML
  "$CHROME" --headless=old --disable-gpu --hide-scrollbars --no-sandbox \
    --force-device-scale-factor=2 --window-size="$W,$H" \
    --screenshot="$DIR/$base.png" "file://$TMP/$base.html" 2>/dev/null
  echo "$base.png  ${W}x${H} @2x"
done
rm -rf "$TMP"
