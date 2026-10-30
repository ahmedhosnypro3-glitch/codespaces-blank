#!/usr/bin/env bash
# Slide 019 Template A full-slide judge, attempt 10 (agent-47 fresh S4b carrier).
# render_17 = current bytes after crop_17-FAIL fixes. Payload: judgeA8_payload_20261024.txt (frozen Template A).
# Polls the vision gate, then dispatches; parks honestly if no window in WAIT_MAX.
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides || exit 1
VID=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$VID/recreated_pptx/qa/slide019
LOG="$Q/legs_status_crops_18_s4.md"
WAIT_MAX="${1:-2400}"
P="$(cat $Q/judgeA8_payload_20261024.txt)"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
note() { echo "[$(ts)] $*" | tee -a "$LOG"; }

t0=$(date +%s)
while :; do
  c=$(pgrep -c -f analyze_image.py 2>/dev/null | head -n1); c="${c:-0}"
  if [ "$c" -lt 8 ]; then break; fi
  el=$(( $(date +%s) - t0 ))
  if [ "$el" -ge "$WAIT_MAX" ]; then
    note "PARK legA10: no window in ${el}s (pgrep=$c); NOT dispatched — honest no-verdict"
    exit 42
  fi
  sleep 20
done
note "WINDOW OPEN (pgrep=$c, waited $(( $(date +%s) - t0 ))s) — DISPATCH legA attempt 10 (render_17)"

timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_17.png $VID/unique_slides/slide_019.jpg \
  --view "Slide 019 recreation attempt 10 - fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_10.txt \
  -p "$P"
rc=$?
el=$(( $(date +%s) - t0 ))
f="$Q/judge_attempt_10.txt"
if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
  note "legA10: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60) (rc=$rc, elapsed ${el}s)"
else
  note "legA10: NO VERDICT (rc=$rc, elapsed ${el}s, transcript $([ -f "$f" ] && echo present-empty || echo MISSING)) — honest no-verdict"
fi
exit 0
