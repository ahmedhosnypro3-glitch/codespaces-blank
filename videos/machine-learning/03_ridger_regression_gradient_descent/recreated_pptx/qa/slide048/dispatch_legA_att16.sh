#!/usr/bin/env bash
# Slide 048 — full-slide Template A judge, attempt 16 (render_16)
set -u
cd /home/codespace/ai_llm_slides
export TMPDIR=/home/codespace/ai_llm_slides/scratch/tmp
mkdir -p "$TMPDIR"
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide048

for _ in $(seq 1 90); do
  n=$(pgrep -c -f analyze_image.py || true)
  n=${n:-0}
  [ "$n" -lt 8 ] && break
  sleep 10
done
echo "=== gate occupancy at dispatch: $(pgrep -c -f analyze_image.py || echo 0) ==="

timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QA/render_16.png" \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_048.jpg \
  --view "Slide 048 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$QA/judge_attempt_16.txt" \
  -p "$(cat "$QA/judge_prompt_1.txt")"
echo "LEG_A_ATT16_RC=$?"
