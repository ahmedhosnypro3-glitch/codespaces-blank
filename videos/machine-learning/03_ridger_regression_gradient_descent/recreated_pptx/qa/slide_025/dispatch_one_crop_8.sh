#!/usr/bin/env bash
# Dispatch ONE slide-025 crop leg (attempt 8, worker-s4-3730479).
# Polls the vision gate, then dispatches crop_8_${SLUG}_render/orig pair with the
# frozen Template-B payload. Never overwrites an existing banked transcript.
set -u
QADIR="/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025"
ROOT="/home/ahmed/Projects/ai_llm_slides"
LOG="$QADIR/legs_status_crops_8_s4.md"
SLUG="$1"; DESC="$2"; WAIT_MAX="${3:-200}"
PAYLOAD="$(cat "$QADIR/crop_prompt_5_${SLUG}.txt")"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
q() { local n; n=$(pgrep -c -f analyze_image.py 2>/dev/null | head -n1); echo "${n:-0}"; }
note() { echo "[$(ts)] $*" | tee -a "$LOG"; }

[ -n "$SLUG" ] || { echo "usage: $0 <slug> <desc> [wait_max]"; exit 2; }
cd "$ROOT"

t0=$(date +%s)
while :; do
  c=$(q)
  if [ "$c" -lt 8 ]; then break; fi
  el=$(( $(date +%s) - t0 ))
  if [ "$el" -ge "$WAIT_MAX" ]; then
    note "PARK $SLUG: no window in ${el}s (pgrep=$c); NOT dispatched — honest no-verdict"
    exit 42
  fi
  sleep 20
done
note "WINDOW OPEN (pgrep=$c, waited $(( $(date +%s) - t0 ))s) — DISPATCH crop $SLUG"

t0=$(date +%s)
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025/crop_8_${SLUG}_render.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025/crop_8_${SLUG}_orig.png \
  --view "Slide 025 zoomed crop ${SLUG} — render vs original at matched scale (attempt 8)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025/crop_8_${SLUG}_judge.txt" \
  -p "$PAYLOAD" >> "$LOG" 2>&1
rc=$?
el=$(( $(date +%s) - t0 ))
f="$QADIR/crop_8_${SLUG}_judge.txt"
if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
  note "crop $SLUG: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60) (rc=$rc, elapsed ${el}s)"
else
  note "crop $SLUG: NO VERDICT (rc=$rc, elapsed ${el}s, transcript $([ -f "$f" ] && echo present-empty || echo MISSING)) — honest no-verdict"
fi
exit 0
