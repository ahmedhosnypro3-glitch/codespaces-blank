#!/usr/bin/env bash
# Slide 042 leg A — full-slide comparison judge (Template A), attempt 24.
# Payload: judge_payload_A_23.txt (content == protocol Template A line 71, wrapper-stripped; no NNN/K tokens).
# Walls: analyzer --timeout 1200 inside `timeout 1700`, --thinking high --max-tokens 65536, --rounds 1 --tries 1.
# Gate law: <8 concurrent analyzers required; bounded backoff then park (rc 42).
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 1
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
GATE="scripts/16_vision_gate.sh"
PY=".agents/skills/image-analysis/scripts/analyze_image.py"
QA="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042"
W="kimi-s6-FRESH-1792954337"

if [ -s "$QA/judge_attempt_24.txt" ]; then echo "LEG A ALREADY BANKED — skip (never double-dispatch)"; exit 0; fi

gate_wait() {
  local tries=0
  while [ "$(pgrep -c -f analyze_image.py)" -ge 8 ]; do
    tries=$((tries+1))
    if [ "$tries" -gt 4 ]; then echo "GATE STILL BUSY after $tries backoffs — PARK (rc 42)"; exit 42; fi
    echo "GATE BUSY ($(pgrep -c -f analyze_image.py)) — backoff $tries/4 (240s)"; python3 scripts/15_progress.py heartbeat 42 "$W" || true
    sleep 240
  done
}

gate_wait
echo "DISPATCH legA K=24 at $(date -Is), gate=$(pgrep -c -f analyze_image.py)"
$GATE timeout 1700 python3 $PY comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/render_24.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_042.jpg \
  --view "Slide 042 recreation attempt 24 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/judge_attempt_24.txt \
  -p "$(cat $QA/judge_payload_A_23.txt)"
echo "LEG A EXIT=$? at $(date -Is)"
