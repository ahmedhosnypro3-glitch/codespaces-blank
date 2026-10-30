#!/bin/bash
set -u
cd /home/ahmed/Projects/ai_llm_slides
DECK=videos/machine-learning/03_ridger_regression_gradient_descent
D=$DECK/recreated_pptx/qa/slide045
n=$(pgrep -c -f analyze_image.py || true)
echo "[legA3] $(date -u +%H:%M:%S) analyzer procs=$n"
if [ "${n:-0}" -ge 8 ]; then echo "[legA3] GATE BUSY"; exit 75; fi
exec timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$D/render_2.png" \
  "$DECK/unique_slides/slide_045.jpg" \
  --view "Slide 045 recreation attempt 3 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$D/judge_attempt_3.txt" \
  -p "$(cat "$D/judge_prompt_1.txt")"
