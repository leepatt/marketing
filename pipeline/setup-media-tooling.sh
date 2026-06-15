#!/usr/bin/env bash
# Craftons media tooling — B9.
# Installs the production pipeline's system + node dependencies.
# Run once locally, OR paste the body into the Claude Code cloud environment's
# "Setup script" field so every session has it cached (recommended for mobile).
set -euo pipefail

SUDO=""
if [ "$(id -u)" -ne 0 ] && command -v sudo >/dev/null 2>&1; then SUDO="sudo"; fi

echo "→ System media tools (ffmpeg, ImageMagick, SVG, fonts)…"
if command -v apt-get >/dev/null 2>&1; then
  $SUDO apt-get update -y
  $SUDO apt-get install -y \
    ffmpeg \
    imagemagick \
    librsvg2-bin \
    fonts-inter \
    fontconfig
fi

# Aeonik is licensed — drop the .otf files from the Drive brain
# (00 Brain/Design-system/fonts/) into ./fonts and uncomment to install system-wide:
# $SUDO mkdir -p /usr/share/fonts/aeonik && $SUDO cp fonts/Aeonik-*.otf /usr/share/fonts/aeonik/ && $SUDO fc-cache -f

echo "→ Node dependencies (playwright, sharp)…"
npm install

echo "→ Playwright Chromium…"
npx playwright install --with-deps chromium

echo "✓ Media tooling ready. Try: npm run render"
