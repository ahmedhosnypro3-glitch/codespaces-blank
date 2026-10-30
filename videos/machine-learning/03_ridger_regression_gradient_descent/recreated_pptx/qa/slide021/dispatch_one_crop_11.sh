#!/usr/bin/env bash
# Dispatch ONE remaining slide-021 crop leg. Polls the gate for up to WAIT_MAX seconds
# (checking before every vision call), then dispatches with the orchestrator's
# --timeout 1200 override inside the unchanged outer timeout 1700 wrapper.
# Command form is dispatch_leg2_crops.sh's run_crop verbatim; payload bytes unchanged.
# Never overwrites an existing banked transcript.
set -u
ROOT="/home/ahmed/Projects/ai_llm_slides"
V="videos/machine-learning/03_ridger_regression_gradient_descent"
QADIR="$ROOT/$V/recreated_pptx/qa/slide021"
LOG="$QADIR/legs_status_crops_11_20261025.md"
WID="worker-s4-3730479"
SLUG="$1"; DESC="$2"; WAIT_MAX="${3:-200}"
PAYLOAD="$(cat "$QADIR/crop_prompt_template_10.txt")"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
q() { local n; n=$(pgrep -c -f analyze_image.py 2>/dev/null | head -n1); echo "${n:-0}"; }
note() { echo "[$(ts)] $*" | tee -a "$LOG"; }

[ -n "$SLUG" ] || { echo "usage: $0 <slug> <desc> [wait_max]"; exit 2; }
cd "$ROOT"

t0=$(date +%s)
while :; do
  el=$(( $(date +%s) - t0 ))
  c=$(q)
  c=${c//[!0-9]/}
  if [ "$c" -lt 8 ]; then break; fi
  if [ "$el" -ge "$WAIT_MAX" ]; then
    note "PARK $SLUG: no window in ${el}s (pgrep=$c); NOT dispatched — honest no-verdict"
    exit 42
  fi
  video_machine_learning_03_ridger_regression_gradient_descent() { :; }
  VIDEO=machine-learning/03_ridger_regression_gradient_descent \
    python3 scripts/15_progress.py heartbeat 21 "$WID" >/dev/null 2>&1
  sleep 20
done
note "WINDOW OPEN (pgrep=$c, waited $(( $(date +%s) - t0 ))s) — DISPATCH crop $SLUG (analyzer --timeout 1200, outer 1700)"

t0=$(date +%s)
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$V/recreated_pptx/qa/slide021/crop_11_${SLUG}_render.png" \
  "$V/recreated_pptx/qa/slide021/crop_11_${SLUG}_orig.png" \
  --view "Slide 021 zoomed crop ${SLUG} — render vs original at matched scale (attempt 11)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$V/recreated_pptx/qa/slide021/crop_11_${SLUG}_judge.txt" \
  -p "$PAYLOAD" >> "$LOG" 2>&1
rc=$?
el=$(( $(date +%s) - t0 ))
f="$QADIR/crop_11_${SLUG}_judge.txt"
if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
  note "crop $SLUG: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60) (rc=$rc, elapsed ${el}s)"
else
  note "crop $SLUG: NO VERDICT (rc=$rc, elapsed ${el}s, transcript $([ -f "$f" ] && echo present-empty || echo MISSING)) — honest no-verdict"
fi
exit 0
