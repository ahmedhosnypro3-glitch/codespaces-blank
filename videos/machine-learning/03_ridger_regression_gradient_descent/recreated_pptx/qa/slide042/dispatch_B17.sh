#!/usr/bin/env bash
# Slide 042 leg B — zoomed crop-pair certificates (Procedure B), attempt 17.
# Payloads byte-for-byte from shared_patterns/judge_protocol_03.md Template B
# with only NNN->042 substituted (word-boundary \bK\b substitution nowhere
# corrupts BLOCKER).
# Walls per orchestrator override: analyzer --timeout 1200 inside `timeout 1700`.
set -u
cd /workspaces/codespaces-blank/ai_llm_slides || exit 1
GATE="scripts/16_vision_gate.sh"
PY="python3 .agents/skills/image-analysis/scripts/analyze_image.py"
QA="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042"

# GATE LAW: back off at >=8 concurrent analyzers
n=$(pgrep -f "python3 .*analyze_image.py" | wc -l)
if [ "${n:-0}" -ge 8 ]; then
  echo "GATE BUSY: $n analyze_image.py running — sleeping 240s"
  VIDEO=machine-learning/03_ridger_regression_gradient_descent \
    python3 scripts/15_progress.py heartbeat 42 w042-finish-20261024 || true
  sleep 240
fi

$GATE timeout 1700 $PY comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_stack_render.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_stack_orig.png \
  --view "Slide 042 zoomed crop stack — render vs original at matched scale (attempt 17)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: the five-box right computation stack: d(x_i) computations, update/keep actions, W result equations" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_stack_judge.txt \
  -p "$(cat $QA/crop_17_stack_prompt.txt)"
echo "LEG B (stack) EXIT=$?"

$GATE timeout 1700 $PY comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_tl_table_render.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_tl_table_orig.png \
  --view "Slide 042 zoomed crop tl_table — render vs original at matched scale (attempt 17)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: top-left vector table: x1..x6 columns, two digit bands, C1/C2 class row, red arrow" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_tl_table_judge.txt \
  -p "$(cat $QA/crop_17_tl_table_prompt.txt)"
echo "LEG B (tl_table) EXIT=$?"

$GATE timeout 1700 $PY comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_lm_table_render.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_lm_table_orig.png \
  --view "Slide 042 zoomed crop lm_table — render vs original at matched scale (attempt 17)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: left-middle upgraded-vectors table: four digit bands, column parens, C1/C2 class row" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_lm_table_judge.txt \
  -p "$(cat $QA/crop_17_lm_table_prompt.txt)"
echo "LEG B (lm_table) EXIT=$?"

$GATE timeout 1700 $PY comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_topright_render.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_topright_orig.png \
  --view "Slide 042 zoomed crop topright — render vs original at matched scale (attempt 17)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: top-right check-classes block: caption, Z1 Z1 Z1 header, two digit rows" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_topright_judge.txt \
  -p "$(cat $QA/crop_17_topright_prompt.txt)"
echo "LEG B (topright) EXIT=$?"

$GATE timeout 1700 $PY comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_legend_render.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_legend_orig.png \
  --view "Slide 042 zoomed crop legend — render vs original at matched scale (attempt 17)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: colour legend sentence: C1 positive, C2 negative, Zero is unaccepted" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/crop_17_legend_judge.txt \
  -p "$(cat $QA/crop_17_legend_prompt.txt)"
echo "LEG B (legend) EXIT=$?"

