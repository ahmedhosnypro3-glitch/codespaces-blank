#!/usr/bin/env bash
# Re-analyze ONE slide via the image-analysis script, default no-params route,
# through the namespace vision gate. Wide wall + one W4 wider-wall retry.
# Usage: run_one.sh <slide-number>
# A degenerate/failed response NEVER overwrites a valid transcript: the attempt
# is banked to failed_slide_NNN_<stamp>.txt and the existing file is kept.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
D="$NS/_pool/audit2"
N=$(printf '%03d' "$1")
IMG="$NS/unique_slides/slide_${N}.jpg"
OUT="$D/slide_${N}.txt"
LOG="$D/run.log"
PROMPT="$NS/_pool/audit_prompt.txt"

valid() { grep -q '\[winner\]' "$1" 2>/dev/null && [ "$(wc -c < "$1" 2>/dev/null || echo 0)" -ge 4000 ]; }
if valid "$OUT"; then echo "slide $N: already valid, skip $(date +%F\ %T)" >> "$LOG"; exit 0; fi

run() { # $1 = --timeout value, $2 = outer wrapper seconds, $3 = attempt tag
  TMP="$D/.slide_${N}.$$.$3.tmp"
  timeout "$2" env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" analysis "$IMG" \
    --timeout "$1" --rounds 1 --tries 1 \
    --view "Slide $N — 'Neural Network Training and Example' lecture slide, printed badge $N" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    -p "$(cat "$PROMPT")" > "$TMP" 2>&1
  if [ -f "$TMP" ]; then
    if valid "$TMP"; then
      mv -f "$TMP" "$OUT"
      echo "slide $N: attempt$3 promoted $(wc -c < "$OUT")B $(date +%F\ %T)" >> "$LOG"
      return 0
    fi
    BANK="$D/failed_slide_${N}_$(date +%F_%H%M%S)_$3.txt"
    mv -f "$TMP" "$BANK"
    echo "slide $N: attempt$3 INVALID ($(wc -c < "$BANK")B) banked to $(basename "$BANK") $(date +%F\ %T)" >> "$LOG"
  else
    echo "slide $N: attempt$3 produced no output file $(date +%F\ %T)" >> "$LOG"
  fi
  return 1
}

echo "slide $N: start $(date +%F\ %T)" >> "$LOG"
run 900 960 1 || true
if ! valid "$OUT"; then
  echo "slide $N: attempt1 invalid — W4 wide retry $(date +%F\ %T)" >> "$LOG"
  sleep 30
  run 1500 1560 2 || true
fi
if valid "$OUT"; then
  echo "slide $N: OK $(wc -c < "$OUT")B $(date +%F\ %T)" >> "$LOG"
else
  echo "slide $N: FAILED — no valid transcript yet $(date +%F\ %T)" >> "$LOG"
fi
