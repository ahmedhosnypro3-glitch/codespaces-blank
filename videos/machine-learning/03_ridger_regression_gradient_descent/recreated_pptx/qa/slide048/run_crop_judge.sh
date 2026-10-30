#!/usr/bin/env bash
# Procedure B crop-pair judge runner for slide 048 (attempt 4), Template B payload VERBATIM.
# Corrected vs scratch/tmp/run_crop_judge.sh: that copy's `cd "$(dirname $0)/.."`
# landed in scratch/tmp (deck root), not the repo root, so every relative path broke.
set -u
NAME="$1"; DESC="$2"
ROOT=/workspaces/codespaces-blank/ai_llm_slides
cd "$ROOT" || exit 2
D="videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$D/recreated_pptx/qa/slide048"
export TMPDIR="$ROOT/$D/scratch/tmp"
TS="$Q/crop_4_${NAME}_judge.txt"
bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/crop_4_${NAME}_render.png" \
  "$Q/crop_4_${NAME}_orig.png" \
  --view "Slide 048 zoomed crop ${NAME} — render vs original at matched scale (attempt 4)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$TS" \
  -p "$(cat "$ROOT/$D/scratch/tmp/payloadB_048_sub.txt")"
rc=$?
echo "CROP_${NAME}_EXIT=$rc $(date -u +%H:%M:%S)"
if grep -q "^FINAL VERDICT:" "$TS" 2>/dev/null; then echo "CROP_${NAME}_VERDICT=$(grep '^FINAL VERDICT:' "$TS")"; else echo "CROP_${NAME}_NO_VERDICT"; fi
exit $rc
