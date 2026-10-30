#!/usr/bin/env bash
# S6 042 LEG A attempt 21 — full-slide Template A on render_21 (post-fix rebuild).
# Payload byte-for-byte from shared_patterns/judge_protocol_03.md (NNN->042),
# verified == judge_prompt_20.txt payload. Walls: --timeout 1200 inside timeout 1700.
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 1
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
GATE="scripts/16_vision_gate.sh"
PY=".agents/skills/image-analysis/scripts/analyze_image.py"
QA="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042"
for i in 1 2 3 4 5 6; do
  n=$(pgrep -f "python3 .*analyze_image.py" | wc -l)
  if [ "${n:-0}" -lt 8 ]; then echo "GATE OK: $n"; break; fi
  echo "GATE BUSY: $n — probe $i, heartbeat + sleep 240"
  VIDEO=machine-learning/03_ridger_regression_gradient_descent \
    python3 scripts/15_progress.py heartbeat 42 kimi-s6-3756628 || true
  sleep 240
  [ "$i" = 6 ] && { echo "PARKED: gate never <8 after 6 probes"; exit 99; }
done
$GATE timeout 1700 python3 $PY comparison \
  $QA/render_21.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_042.jpg \
  --view "Slide 042 recreation attempt 21 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $QA/judge_attempt_21.txt \
  -p "$(cat $QA/judge_prompt_20.txt)"
echo "LEG A (attempt 21) EXIT=$?"
