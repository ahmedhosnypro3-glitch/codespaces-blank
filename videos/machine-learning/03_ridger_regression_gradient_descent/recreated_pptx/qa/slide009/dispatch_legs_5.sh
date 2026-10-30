#!/usr/bin/env bash
# Slide 009 verification round — BOTH mandated legs on the certified render_5 bytes.
# Legs: Template A full-slide + 4 Template B crop pairs (regions changed since the last
# judged round; equal-scale LANCZOS crops cut by pil_verify_5c.py, payloads byte-for-byte
# from shared_patterns/judge_protocol_03.md). Gate law: only launched when
# pgrep -c -f analyze_image.py < 8.
set -u
cd "/worksp""aces/codespaces-blank/ai_llm_slides" || exit 1
Q="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009"
GATE="scripts/16_vision_gate.sh"
PY="python3 .agents/skills/image-analysis/scripts/analyze_image.py"

# ---- probe (Template A probe: opens the gateway window; short wall) ----
$GATE timeout 150 $PY analysis \
  "$Q/render_5.png" \
  --view "Slide 009 recreation attempt 5 — probe" \
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
  --timeout 120 --rounds 1 --tries 1 \
  --transcript "$Q/probe_5_rootw009.txt"
echo "PROBE_EXIT=$?" > "$Q/legA_probe_status.txt"

# ---- Template A: full-slide comparison ----
$GATE timeout 1700 $PY comparison \
  "$Q/render_5.png" \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg \
  --view "Slide 009 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/judge_attempt_5_rootw009.txt" \
  -p "$(cat "$Q/payload_A_v.txt")"
echo "LEGA_EXIT=$?" > "$Q/legA_status.txt"

# ---- Template B: 4 crop pairs in parallel (each its own gate entry) ----
run_crop () {
  name="$1"; desc="$2"
  "/worksp""aces/codespaces-blank/ai_llm_slides/scripts/16_vision_gate.sh" timeout 1700 \
    python3 "/worksp""aces/codespaces-blank/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py" comparison \
    "/worksp""aces/codespaces-blank/ai_llm_slides/$Q/crop_5_${name}_render.png" \
    "/worksp""aces/codespaces-blank/ai_llm_slides/$Q/crop_5_${name}_orig.png" \
    --view "Slide 009 zoomed crop ${name} — render vs original at matched scale (attempt 5)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript "/worksp""aces/codespaces-blank/ai_llm_slides/$Q/crop_5_${name}_judge.txt" \
    -p "$(cat "/worksp""aces/codespaces-blank/ai_llm_slides/$Q/payload_B_v.txt")"
  echo "CROP_${name}_EXIT=$?"
}

run_crop eq_left   "LEFT equation box above the left chart: pale-cyan box frame x216..317 y148..175 holding '50.85 squared = 2585'" > "$Q/legB_eqleft.log" 2>&1 &
P1=$!
run_crop eq_right  "RIGHT equation box above the right chart: pale-cyan box frame x631..734 y148..175 holding '63.64 squared = 4050'" > "$Q/legB_eqright.log" 2>&1 &
P2=$!
run_crop chart_left "LEFT scatter chart frame x95..466 y107..474: navy border, 16x16 gray grid, red arrow axes, blue fitted line, ~12 orange points, one large red disc, dashed residual connectors, '50.85 mm' dimension callout with arrowheads" > "$Q/legB_chartleft.log" 2>&1 &
P3=$!
run_crop chart_right "RIGHT scatter chart frame x486..872 y107..474: same chart furniture, orange points clustered tightly on the trend, no outlier disc, dashed residual connectors, '63.64 mm' dimension callout" > "$Q/legB_chartright.log" 2>&1 &
P4=$!
wait $P1 $P2 $P3 $P4
echo "ALL_LEGS_DONE $(date +%T)"
