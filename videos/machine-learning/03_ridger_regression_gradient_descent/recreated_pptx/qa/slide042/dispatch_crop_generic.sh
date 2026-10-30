#!/usr/bin/env bash
# S6 042 LEG B crop — NAME/K/RENDER args; Template B payload 042 (byte-verified 1924B).
# GATE_OK precheck passed by caller. Walls: --timeout 1200 inside timeout 1700.
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 1
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
GATE="scripts/16_vision_gate.sh"
PY=".agents/skills/image-analysis/scripts/analyze_image.py"
QA="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042"
NAME="$1"; K="$2"; RENDER="$3"; PAIRK="$4"; REGION="$5"
$GATE timeout 1700 python3 $PY comparison \
  $QA/crop_${PAIRK}_${NAME}_render.png \
  $QA/crop_${PAIRK}_${NAME}_orig.png \
  --view "Slide 042 zoomed crop $NAME — render vs original at matched scale (attempt $K)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $REGION" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $QA/crop_${K}_${NAME}_judge.txt \
  -p "$(cat $QA/crop_23_topright_payload.txt)"
echo "CROP $NAME (attempt $K, pair $PAIRK) EXIT=$?"
