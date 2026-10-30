#!/usr/bin/env bash
# Slide 025 Template A full-slide judge on render_12 (attempt 12, S4b finisher).
# Adapted from staged dispatch_A_6.sh (render_6/attempt 6); wall 1200 preserved.
# Payload: judge_prompt_4.txt (frozen Template A, byte-identical to judge_protocol_03.md Template A).
# Usage: dispatch_A12_1200.sh [wait_max]
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides || exit 1
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025
WAIT_MAX="${1:-900}"
LOG="$Q/legs_status_crops_10_s4.md"
P="$(cat $Q/judge_prompt_4.txt)"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
note() { echo "[$(ts)] A25: $*" | tee -a "$LOG"; }

t0=$(date +%s)
while :; do
  c=$(pgrep -c -f analyze_image.py 2>/dev/null | head -n1); c="${c:-0}"
  if [ "$c" -lt 8 ]; then break; fi
  el=$(( $(date +%s) - t0 ))
  if [ "$el" -ge "$WAIT_MAX" ]; then
    note "PARK A25: no window in ${el}s (pgrep=$c); NOT dispatched — honest no-verdict"
    exit 42
  fi
  sleep 20
done
note "WINDOW OPEN (pgrep=$c, waited $(( $(date +%s) - t0 ))s) — DISPATCH Template A render_12 (attempt 12)"

timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_12.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg \
  --view "Slide 025 recreation attempt 12 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_12.txt \
  -p "$P" >> "$LOG" 2>&1
rc=$?
f="$Q/judge_attempt_12.txt"
if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
  note "Template A attempt 12: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60) (rc=$rc)"
else
  note "Template A attempt 12: NO VERDICT (rc=$rc) — honest no-verdict"
fi
exit 0
