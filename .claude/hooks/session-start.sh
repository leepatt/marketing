#!/bin/bash
# SessionStart hook — ensure media tooling is present for every (web) session.
# Installs: ffmpeg (frame extraction for tools/video-frames.py + future video
# assembly), ImageMagick/SVG/fonts (pipeline/ render), Python imaging deps, and
# pipeline node deps. Idempotent and non-interactive. Chromium is pre-installed
# in this environment, so we deliberately skip `playwright install`.
set -euo pipefail

# Only needed in the remote (Claude Code on the web) environment.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

log() { echo "[session-start] $*"; }

SUDO=""
if [ "$(id -u)" -ne 0 ] && command -v sudo >/dev/null 2>&1; then SUDO="sudo"; fi

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"

# 1) System media tools via apt (idempotent; skipped if ffmpeg already present).
if ! command -v ffmpeg >/dev/null 2>&1; then
  log "ffmpeg missing — installing media tools via apt…"
  if command -v apt-get >/dev/null 2>&1; then
    # The package index is stale in fresh containers and 404s on .deb fetches
    # unless refreshed first.
    $SUDO apt-get update -y >/dev/null 2>&1 || true
    $SUDO apt-get install -y ffmpeg imagemagick librsvg2-bin fonts-inter fontconfig >/dev/null 2>&1 || true
  fi
fi

# 2) Fallback: static ffmpeg via pip if apt couldn't provide it (keeps frame
#    extraction working even when apt is broken).
if ! command -v ffmpeg >/dev/null 2>&1; then
  log "apt ffmpeg unavailable — falling back to imageio-ffmpeg static binary…"
  pip install --quiet imageio-ffmpeg >/dev/null 2>&1 || true
  FF="$(python3 -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())' 2>/dev/null || true)"
  if [ -n "${FF:-}" ] && [ ! -e /usr/local/bin/ffmpeg ]; then
    $SUDO ln -sf "$FF" /usr/local/bin/ffmpeg 2>/dev/null || ln -sf "$FF" /usr/local/bin/ffmpeg || true
  fi
fi

if command -v ffmpeg >/dev/null 2>&1; then
  log "ffmpeg ready: $(command -v ffmpeg)"
else
  log "WARNING: ffmpeg still unavailable after apt + pip fallback"
fi

# 3) Python imaging deps for tools/video-frames.py (perceptual-hash dedupe).
if ! python3 -c "import PIL, imagehash" >/dev/null 2>&1; then
  log "installing Python imaging deps (Pillow, imagehash)…"
  pip install --quiet Pillow imagehash >/dev/null 2>&1 || true
fi

# 4) Node deps for the pipeline/ render engine (Chromium already pre-installed).
if [ -f "$PROJECT_DIR/pipeline/package.json" ] && [ ! -d "$PROJECT_DIR/pipeline/node_modules" ]; then
  log "installing pipeline node deps (playwright, sharp)…"
  (cd "$PROJECT_DIR/pipeline" && npm install --no-audit --no-fund >/dev/null 2>&1) || true
fi

log "media tooling ready."
