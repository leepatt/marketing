#!/usr/bin/env bash
# Re-render the composition locally. No HeyGen account or MCP connector needed.
# Usage:  ./render.sh            → out/formwork-builder-reel.mp4
#         ./render.sh check      → lint + runtime + layout + contrast gate only
#         ./render.sh snapshot   → PNG frames at key beats into snapshots/
set -euo pipefail
cd "$(dirname "$0")"
TOOLS="${HYPERFRAMES_TOOLS_DIR:-$HOME/.cache/craftons-hyperframes}"
if [ ! -x "$TOOLS/node_modules/.bin/hyperframes" ]; then
  mkdir -p "$TOOLS" && cd "$TOOLS" && npm init -y >/dev/null 2>&1
  PUPPETEER_SKIP_DOWNLOAD=1 npm install --no-audit --no-fund hyperframes@0.8.34 @ffmpeg-installer/linux-x64 @ffprobe-installer/linux-x64
  cd - >/dev/null
fi
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1
export HYPERFRAMES_FFMPEG_PATH="$TOOLS/node_modules/@ffmpeg-installer/linux-x64/ffmpeg"
export HYPERFRAMES_FFPROBE_PATH="$TOOLS/node_modules/@ffprobe-installer/linux-x64/ffprobe"
chmod +x "$HYPERFRAMES_FFMPEG_PATH" "$HYPERFRAMES_FFPROBE_PATH" 2>/dev/null || true
# Chrome: Playwright's bundle in the Claude web sandbox; otherwise let hyperframes find/manage one.
for c in /opt/pw-browsers/chromium-*/chrome-linux/chrome /usr/bin/chromium /usr/bin/google-chrome; do
  [ -x "$c" ] && export HYPERFRAMES_BROWSER_PATH="$c" && break
done
# Aeonik is licensed and git-ignored. Declare it only if the file is here (see README for the Drive id).
if [ -f fonts/Aeonik-Medium.otf ]; then
  printf '@font-face { font-family: "Aeonik"; src: url("Aeonik-Medium.otf") format("opentype"); font-weight: 500; font-style: normal; }\n' > fonts/aeonik.css
else
  printf '/* fonts/Aeonik-Medium.otf not present: display face falls back to Inter. See README. */\n' > fonts/aeonik.css
  echo "note: fonts/Aeonik-Medium.otf missing, rendering with Inter as the display face" >&2
fi
HF="$TOOLS/node_modules/.bin/hyperframes"
case "${1:-render}" in
  check)    "$HF" check ;;
  snapshot) "$HF" snapshot --at 3,12,20,27,35,50,62,75,96.5 --no-end --describe false -o snapshots ;;
  *)        mkdir -p out && "$HF" render -o "out/formwork-builder-reel.mp4" ;;
esac
