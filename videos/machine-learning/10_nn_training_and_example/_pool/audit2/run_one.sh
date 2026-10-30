#!/usr/bin/env bash
# Re-analyze ONE slide via the image-analysis script, default no-params route,
# through the namespace vision gate. Wide wall + one W4 wider-wall retry.
# Usage: run_one.sh <slide-number>
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
N=$(printf '%03d' "$1")
IMG="$NS/unique_slides/slide_${N}.jpg"
OUT="$NS/_pool/audit2/slide_${N}.txt"
LOG="$NS/_pool/audit2/run.log"
PROMPT="$NS/_pool/audit_prompt.txt"

valid() { grep -q '\[winner\]' "$OUT" 2>/dev/null && [ "$(wc -c < "$OUT" 2>/dev/null || echo 0)" -ge 4000 ]; }
if valid; then echo "slide $N: already valid, skip $(date +%F\ %T)" >> "$LOG"; exit 0; fi

run() { # $1 = --timeout value, $2 = outer wrapper seconds
  timeout "$2" env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" analysis "$IMG" \
    --timeout "$1" --rounds 1 --tries 1 \
    --view "Slide $N — 'Neural Network Training and Example' lecture slide, printed badge $N" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    -p "$(cat "$PROMPT")" > "$OUT.tmp" 2>&1
  mv "$OUT.tmp" "$OUT"
}

echo "slide $N: start $(date +%F\ %T)" >> "$LOG"
run 900 960
if ! valid; then
  echo "slide $N: attempt1 invalid ($(wc -c < "$OUT")B) — W4 wide retry $(date +%F\ %T)" >> "$LOG"
  sleep 30
  run 1500 1560
fi
if valid; then
  echo "slide $N: OK $(wc -c < "$OUT")B $(date +%F\ %T)" >> "$LOG"
else
  echo "slide $N: FAILED bytes=$(wc -c < "$OUT") $(date +%F\ %T)" >> "$LOG"
fi
