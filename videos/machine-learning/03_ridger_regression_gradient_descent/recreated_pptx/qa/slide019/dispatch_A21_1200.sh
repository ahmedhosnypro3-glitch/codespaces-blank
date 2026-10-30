#!/usr/bin/env bash
# Slide 019 Template A full-slide judge on render_21 (attempt 21, S4b finisher).
# render_21 = post-fix bytes: outlierRow single-line digit boxes (9/9 colored,
# 30/60 red), W-enclosure + grid-outer rects maroon.
# Payload: judgeA8_payload_20261024.txt (frozen Template A, md5-verified vs judge_protocol_03.md).
# Usage: dispatch_A21_1200.sh [wait_max]
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides || exit 1
VID=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$VID/recreated_pptx/qa/slide019
WAIT_MAX="${1:-1800}"
LOG="$Q/legs_status_21_s4b.md"
P="$(cat $Q/judgeA8_payload_20261024.txt)"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
note() { echo "[$(ts)] A21: $*" | tee -a "$LOG"; }

t0=$(date +%s)
while :; do
  c=$(pgrep -c -f analyze_image.py 2>/dev/null | head -n1); c="${c:-0}"
  if [ "$c" -lt 8 ]; then break; fi
  el=$(( $(date +%s) - t0 ))
  if [ "$el" -ge "$WAIT_MAX" ]; then
    note "PARK A21: no window in ${el}s (pgrep=$c); NOT dispatched — honest no-verdict"
    exit 42
  fi
  sleep 20
done
note "WINDOW OPEN (pgrep=$c, waited $(( $(date +%s) - t0 ))s) — DISPATCH Template A render_21 (attempt 21)"

timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_21.png $VID/unique_slides/slide_019.jpg \
  --view "Slide 019 recreation attempt 21 - fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_21.txt \
  -p "$P" >> "$LOG" 2>&1
rc=$?
f="$Q/judge_attempt_21.txt"
if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
  note "Template A attempt 21: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60) (rc=$rc)"
else
  note "Template A attempt 21: NO VERDICT (rc=$rc) — honest no-verdict"
fi
exit 0
