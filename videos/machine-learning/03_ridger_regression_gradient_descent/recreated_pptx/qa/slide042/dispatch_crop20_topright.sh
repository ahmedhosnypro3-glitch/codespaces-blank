#!/usr/bin/env bash
# S6 042 crop leg — topright on the UNCHANGED crop_20 pair (region pixel-identical r20->r21).
# Arbitrates pending Q1 (InitialW third component) + Q3 (Z vector row counts).
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 1
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
GATE="scripts/16_vision_gate.sh"
PY=".agents/skills/image-analysis/scripts/analyze_image.py"
QA="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042"
for i in 1 2 3 4 5 6; do
  n=$(pgrep -f "python3 .*analyze_image.py" | wc -l)
  if [ "${n:-0}" -lt 8 ]; then echo "GATE OK: $n"; break; fi
  echo "GATE BUSY: $n — probe $i"; sleep 240
  [ "$i" = 6 ] && { echo "PARKED: gate never <8 after 6 probes"; exit 99; }
done
$GATE timeout 1700 python3 $PY comparison \
  $QA/crop_20_topright_render.png $QA/crop_20_topright_orig.png \
  --view "Slide 042 zoomed crop topright — render vs original at matched scale (attempt 20)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: top-right check-classes block: caption, Z1 Z1 Z1 header, two digit rows" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $QA/crop_20_topright_judge.txt \
  -p "$(cat $QA/crop_18_topright_prompt.txt)"
echo "CROP TOPRIGHT (attempt 20) EXIT=$?"
