#!/usr/bin/env bash
# Slide 019 crop leg — attempt 28 on render_27 (post-fix bytes: outlierRow
# single-line digit boxes 9/9 colored, 30/60 red; W-enclosure + grid-outer
# rects maroon). Crops cut from render_27 (crop_27_* names kept).
# Usage: dispatch_B21_1200.sh <slug> <desc> [wait_max]
# Slugs: header_strip, noreg_rows, table_left, table_right
set -u
QADIR="/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019"
ROOT="/home/ahmed/Projects/ai_llm_slides"
LOG="$QADIR/legs_status_27_s4b.md"
SLUG="$1"; DESC="$2"; WAIT_MAX="${3:-1800}"
PAYF="$QADIR/judgeB8_payload_20261024.txt"
[ -n "$SLUG" ] || { echo "usage: $0 <slug> <desc> [wait_max]"; exit 2; }
[ -s "$PAYF" ] || { echo "FATAL: payload $PAYF missing/empty — NOT dispatching" | tee -a "$LOG"; exit 3; }
PAYLOAD="$(cat "$PAYF")"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
q() { local n; n=$(pgrep -c -f analyze_image.py 2>/dev/null | head -n1); echo "${n:-0}"; }
note() { echo "[$(ts)] $*" | tee -a "$LOG"; }

cd "$ROOT"

t0=$(date +%s)
while :; do
  c=$(q)
  if [ "$c" -lt 8 ]; then break; fi
  el=$(( $(date +%s) - t0 ))
  if [ "$el" -ge "$WAIT_MAX" ]; then
    note "PARK crop_27 $SLUG: no window in ${el}s (pgrep=$c); NOT dispatched — honest no-verdict"
    exit 42
  fi
  sleep 20
done
note "WINDOW OPEN (pgrep=$c, waited $(( $(date +%s) - t0 ))s) — DISPATCH crop_27 $SLUG"

t0=$(date +%s)
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QADIR/crop_27_${SLUG}_render.png" \
  "$QADIR/crop_27_${SLUG}_orig.png" \
  --view "Slide 019 zoomed crop ${SLUG} — render vs original at matched scale (attempt 28)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$QADIR/crop_27_${SLUG}_judge.txt" \
  -p "$PAYLOAD" >> "$LOG" 2>&1
rc=$?
el=$(( $(date +%s) - t0 ))
f="$QADIR/crop_27_${SLUG}_judge.txt"
if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
  note "crop_27 $SLUG: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60) (rc=$rc, elapsed ${el}s)"
else
  note "crop_27 $SLUG: NO VERDICT (rc=$rc, elapsed ${el}s, transcript $([ -f "$f" ] && echo present-empty || echo MISSING)) — honest no-verdict"
fi
exit 0
