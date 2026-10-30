#!/usr/bin/env bash
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 1
GATE="scripts/16_vision_gate.sh"
PY="python3 .agents/skills/image-analysis/scripts/analyze_image.py"
QA="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042"
n=$(pgrep -f "python3 .*analyze_image.py" | wc -l)
if [ "${n:-0}" -ge 8 ]; then echo "GATE BUSY: $n"; sleep 240; fi
$GATE timeout 1700 $PY comparison \
  $QA/crop_18_stack_render.png $QA/crop_18_stack_orig.png \
  --view "Slide 042 zoomed crop STACK — render vs original at matched scale (attempt 18)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: the right computation stack: five white boxes each holding a d(x_i) matrix line, a result, an arrow, an action phrase and a W-equation line" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $QA/crop_18_stack_judge.txt \
  -p "$(cat $QA/crop_18_stack_prompt.txt)"
echo "CROP STACK EXIT=$?"
