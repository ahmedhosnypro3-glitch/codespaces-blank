#!/usr/bin/env bash
# Regenerate wave-2 audit for slide 023 (truncated transcript) with a raised
# token budget. Private temp path so it cannot collide with the dispatcher's
# shared .tmp. Storm clause: 120s sleep, up to 3 retries.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
OUT="$NS/_pool/audit2/slide_023.txt"
TMP="$NS/_pool/audit2/.slide_023.regen.$$"
LOG="$NS/_pool/audit2/slide_023_regen.log"

run() { # $1 analyze --timeout, $2 outer timeout seconds
  timeout "$2" env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" analysis "$NS/unique_slides/slide_023.jpg" \
    --timeout "$1" --rounds 1 --tries 1 --max-tokens 32768 \
    --view "Slide 023 — 'Neural Network Training and Example' lecture slide, printed badge 023" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    -p "$(cat "$NS/_pool/audit_prompt.txt")" > "$TMP" 2>&1
  echo "run wall=$1 outer=$2 rc=$? bytes=$(wc -c < "$TMP") $(date -u +%T)" >> "$LOG"
}

# valid = [winner] present, >=4000 bytes, a verdict section, no truncation warn
valid() {
  grep -q '\[winner\]' "$TMP" 2>/dev/null \
    && [ "$(wc -c < "$TMP")" -ge 4000 ] \
    && grep -qi 'verdict' "$TMP" \
    && ! grep -q 'likely TRUNCATED' "$TMP"
}

echo "=== slide023 audit regen start $(date -u +%FT%TZ) ===" >> "$LOG"
for i in 1 2 3 4; do
  run 900 1140
  if valid; then
    cp "$TMP" "$OUT"
    echo "AUDIT_023_VALID bytes=$(wc -c < "$OUT") attempt=$i $(date -u +%T)" >> "$LOG"
    echo "AUDIT_023_VALID bytes=$(wc -c < "$OUT")"
    rm -f "$TMP"
    exit 0
  fi
  echo "attempt=$i invalid bytes=$(wc -c < "$TMP") — storm sleep 120" >> "$LOG"
  [ "$i" = "4" ] || sleep 120
done
echo "AUDIT_023_INVALID bytes=$(wc -c < "$OUT")"
rm -f "$TMP"
exit 1
