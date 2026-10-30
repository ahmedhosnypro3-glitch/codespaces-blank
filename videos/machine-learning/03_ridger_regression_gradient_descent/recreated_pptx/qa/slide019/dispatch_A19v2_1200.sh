#!/usr/bin/env bash
# Slide 019 Template A full-slide judge on render_19 (attempt 19, S4b fresh).
# Attempt 19 bytes: 0.64/0.77/1.1, parens-46, header tints, white table body,
# bottom tint strip (banked pre-fix backup: build_slide019_prefixfix2_backup_20261025.js).
# Payload: judgeA8_payload_20261024.txt (frozen Template A, md5-verified vs judge_protocol_03.md).
# Usage: dispatch_A19v2_1200.sh [wait_max]
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides || exit 1
VID=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$VID/recreated_pptx/qa/slide019
WAIT_MAX="${1:-900}"
LOG="$Q/legs_status_19_fresh_s4b.md"
P="$(cat $Q/judgeA8_payload_20261024.txt)"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
note() { echo "[$(ts)] A19v2: $*" | tee -a "$LOG"; }

t0=$(date +%s)
while :; do
  c=$(pgrep -c -f analyze_image.py 2>/dev/null | head -n1); c="${c:-0}"
  if [ "$c" -lt 8 ]; then break; fi
  el=$(( $(date +%s) - t0 ))
  if [ "$el" -ge "$WAIT_MAX" ]; then
    note "PARK A19v2: no window in ${el}s (pgrep=$c); NOT dispatched — honest no-verdict"
    exit 42
  fi
  sleep 20
done
note "WINDOW OPEN (pgrep=$c, waited $(( $(date +%s) - t0 ))s) — DISPATCH Template A render_19 (attempt 19)"

timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_19.png $VID/unique_slides/slide_019.jpg \
  --view "Slide 019 recreation attempt 19 - fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_19.txt \
  -p "$P" >> "$LOG" 2>&1
rc=$?
f="$Q/judge_attempt_19.txt"
if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
  note "Template A attempt 19: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60) (rc=$rc)"
else
  note "Template A attempt 19: NO VERDICT (rc=$rc) — honest no-verdict"
fi
exit 0
