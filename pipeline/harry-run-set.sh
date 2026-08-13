#!/bin/bash
# Drive the remaining Harry shots unattended, holding the same gates.
#
#   harry-run-set.sh <sandbox-dir> <first-shot> <last-shot>
#
# Per shot: roll a block of 6 candidates, and if none clears both gates — face
# >= 0.90 against the hero AND the scene actually changed — roll another block of
# fresh seeds, up to 4 blocks. Anything that clears is moved straight to
# approved/, because later shots build on earlier ones and need them there.
#
# A shot that never clears in 24 attempts is left in candidates/ and recorded in
# the log as UNRESOLVED rather than quietly promoted. Better to hand back a short
# set with a known gap than a full one with a frame nobody checked.
set -uo pipefail

SANDBOX="$1"; FIRST="$2"; LAST="$3"
HERO="$SANDBOX/hero/HARRY-HERO.png"
LOG="$SANDBOX/run.log"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Harry set: shots $FIRST-$LAST, started $(date -u +%H:%M:%SZ) ===" | tee -a "$LOG"

for n in $(seq "$FIRST" "$LAST"); do
  cleared=0
  for block in 0 6 12 18; do
    echo "--- shot $n, seed block $block" | tee -a "$LOG"
    # Capture the exit status directly. Piping the run into tee makes the
    # pipeline's status tee's, not the generator's, so every shot reads as
    # cleared and the gate silently stops gating. pipefail covers it here, but
    # the quick one-off drivers written without it promoted four failing frames
    # before this was caught — so don't rely on the shell option being set.
    out=$(mktemp)
    if python3 "$HERE/harry-shoot.py" "$HERO" "$SANDBOX/candidates" "$n" 6 "$block" > "$out" 2>&1; then
      cleared=1
    fi
    grep -vE "^(Applied|find model|set det|download|/usr/local|  tform)" "$out" | tee -a "$LOG"
    rm -f "$out"
    [ "$cleared" = 1 ] && break
  done

  f=$(ls "$SANDBOX/candidates"/$(printf '%02d' "$n")-*.png 2>/dev/null | head -1)
  if [ "$cleared" = "1" ] && [ -n "$f" ]; then
    mv "$f" "$SANDBOX/approved/"
    echo "shot $n APPROVED -> $(basename "$f")" | tee -a "$LOG"
  else
    echo "shot $n UNRESOLVED — best candidate left in candidates/ for review" | tee -a "$LOG"
  fi
done

echo "=== finished $(date -u +%H:%M:%SZ) ===" | tee -a "$LOG"
echo "approved: $(ls "$SANDBOX/approved" | wc -l)   unresolved: $(ls "$SANDBOX/candidates"/*.png 2>/dev/null | wc -l)" | tee -a "$LOG"
