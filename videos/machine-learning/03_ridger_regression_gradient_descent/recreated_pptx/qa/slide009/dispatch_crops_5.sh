#!/usr/bin/env bash
# Slide 009 verification round — Template B crop legs only (4 regions changed since the
# last judged round; transcript names carry _rootw009_ to never clobber the prior lane's
# banked crop_5_<name>_judge.txt, preserved as crop_5_lane_<name>_judge.txt).
set -u
cd "/worksp""aces/codespaces-blank/ai_llm_slides" || exit 1
Q="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009"
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"

run_crop () {
  name="$1"; desc="$2"
  "$ROOT/scripts/16_vision_gate.sh" timeout 1700 \
    python3 "$ROOT/.agents/skills/image-analysis/scripts/analyze_image.py" comparison \
    "$ROOT/$Q/crop_5_${name}_render.png" \
    "$ROOT/$Q/crop_5_${name}_orig.png" \
    --view "Slide 009 zoomed crop ${name} — render vs original at matched scale (attempt 5, independent verification worker w009-root-20261024)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript "$ROOT/$Q/crop_5_rootw009_${name}_judge.txt" \
    -p "$(cat "$ROOT/$Q/payload_B_v.txt")"
  echo "CROP_${name}_EXIT=$?"
}

run_crop eq_left     "LEFT equation box above the left chart: pale-cyan box frame x216..317 y148..175 holding '50.85 squared = 2585'" > "$Q/legB_eqleft.log" 2>&1 &
P1=$!
run_crop eq_right    "RIGHT equation box above the right chart: pale-cyan box frame x631..734 y148..175 holding '63.64 squared = 4050'" > "$Q/legB_eqright.log" 2>&1 &
P2=$!
run_crop chart_left  "LEFT scatter chart frame x95..466 y107..474: navy border, 16x16 gray grid, red arrow axes, blue fitted line, ~12 orange points, one large red disc, dashed residual connectors, '50.85 mm' dimension callout with arrowheads" > "$Q/legB_chartleft.log" 2>&1 &
P3=$!
run_crop chart_right "RIGHT scatter chart frame x486..872 y107..474: same chart furniture, orange points clustered tightly on the trend, no outlier disc, dashed residual connectors, '63.64 mm' dimension callout" > "$Q/legB_chartright.log" 2>&1 &
P4=$!
wait $P1 $P2 $P3 $P4
echo "CROPS_DONE $(date +%T)"
