#!/usr/bin/env bash
# Slide 025 Template A full-slide judge, attempt 7 (agent-47 fresh S4b carrier).
# render_12 = current bytes after K=11 fixes. Payload: judge_prompt_4.txt (frozen Template A).
# Polls the vision gate, then dispatches; parks honestly if no window in WAIT_MAX.
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides || exit 1
VID=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$VID/recreated_pptx/qa/slide_025
LOG="$Q/legs_status_crops_10_s4.md"
WAIT_MAX="${1:-2400}"
P="$(cat $Q/judge_prompt_4.txt)"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
note() { echo "[$(ts)] $*" | tee -a "$LOG"; }

t0=$(date +%s)
while :; do
  c=$(pgrep -c -f analyze_image.py 2>/dev/null | head -n1); c="${c:-0}"
  if [ "$c" -lt 8 ]; then break; fi
  el=$(( $(date +%s) - t0 ))
  if [ "$el" -ge "$WAIT_MAX" ]; then
    note "PARK legA7: no window in ${el}s (pgrep=$c); NOT dispatched — honest no-verdict"
    exit 42
  fi
  sleep 20
done
note "WINDOW OPEN (pgrep=$c, waited $(( $(date +%s) - t0 ))s) — DISPATCH legA attempt 7 (render_12)"

timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_12.png $VID/unique_slides/slide_025.jpg \
  --view "Slide 025 recreation attempt 7 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_7.txt \
  -p "$P"
rc=$?
el=$(( $(date +%s) - t0 ))
f="$Q/judge_attempt_7.txt"
if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
  note "legA7: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60) (rc=$rc, elapsed ${el}s)"
else
  note "legA7: NO VERDICT (rc=$rc, elapsed ${el}s, transcript $([ -f "$f" ] && echo present-empty || echo MISSING)) — honest no-verdict"
fi
exit 0
