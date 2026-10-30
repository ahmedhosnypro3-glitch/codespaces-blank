#!/usr/bin/env bash
# Slide 025 crop leg — attempt 14 on render_14 (k13 bytes). Crops cut by
# cut_crops_14.py (crop_14_<slug>_*). Payloads: per-slug crop_prompt_4_<slug>.txt
# (frozen Template B, NNN->025, byte-verified in verify_4.txt).
# Usage: dispatch_B14_1200.sh <slug> <desc> [wait_max]
# Slugs: title, lbl_upper, lbl_lower, tl, tr, bl, br
set -u
QADIR="/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025"
ROOT="/home/ahmed/Projects/ai_llm_slides"
LOG="$QADIR/legs_status_14_s4b.md"
SLUG="$1"; DESC="$2"; WAIT_MAX="${3:-1800}"
[ -n "$SLUG" ] || { echo "usage: $0 <slug> <desc> [wait_max]"; exit 2; }
PAYF="$QADIR/crop_prompt_4_${SLUG}.txt"
[ -s "$PAYF" ] || { echo "FATAL: payload $PAYF missing/empty — NOT dispatching" | tee -a "$LOG"; exit 3; }
[ -s "$QADIR/crop_14_${SLUG}_render.png" ] || { echo "FATAL: crop_14_${SLUG}_render.png missing — run cut_crops_14.py" | tee -a "$LOG"; exit 3; }
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
    note "PARK crop_14 $SLUG: no window in ${el}s (pgrep=$c); NOT dispatched — honest no-verdict"
    exit 42
  fi
  sleep 20
done
note "WINDOW OPEN (pgrep=$c, waited $(( $(date +%s) - t0 ))s) — DISPATCH crop_14 $SLUG"

t0=$(date +%s)
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QADIR/crop_14_${SLUG}_render.png" \
  "$QADIR/crop_14_${SLUG}_orig.png" \
  --view "Slide 025 zoomed crop ${SLUG} — render vs original at matched scale (attempt 14)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$QADIR/crop_14_${SLUG}_judge.txt" \
  -p "$PAYLOAD" >> "$LOG" 2>&1
rc=$?
el=$(( $(date +%s) - t0 ))
f="$QADIR/crop_14_${SLUG}_judge.txt"
if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
  note "crop_14 $SLUG: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60) (rc=$rc, elapsed ${el}s)"
else
  note "crop_14 $SLUG: NO VERDICT (rc=$rc, elapsed ${el}s, transcript $([ -f "$f" ] && echo present-empty || echo MISSING)) — honest no-verdict"
fi
exit 0
