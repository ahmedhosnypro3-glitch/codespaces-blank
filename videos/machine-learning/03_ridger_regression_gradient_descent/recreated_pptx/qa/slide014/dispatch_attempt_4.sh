#!/usr/bin/env bash
# Slide 014 FINAL CERTIFICATION LEGS (attempt 4, the PIL-measured rebuild).
# Payloads byte-verified from shared_patterns/judge_protocol_03.md:
#   Template A md5 9387f5fbb94ef05a31db19f1e018dde1 (no standalone K)
#   Template B md5 978be75de7b83501d09f8f0c5576cbee (\bK\b -> 4)
# Render render_4.png (chrome PASS); crops crop_4_{bands,vectors,final} at
# matched scale. Gate law: congestion probe before EACH leg; >= 8 -> exit 42.
set -u
ROOT="/workspaces/codespaces-blank/ai_llm_slides"
DECK="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$DECK/recreated_pptx/qa/slide014"
PY=".agents/skills/image-analysis/scripts/analyze_image.py"
export TMPDIR="$ROOT/scratch/tmp"
mkdir -p "$TMPDIR"

n=$(pgrep -c -f analyze_image.py || true)
echo "=== [$(date -u +%FT%TZ)] congestion probe: $n analyze_image.py ==="
if [ "$n" -ge 8 ]; then
  echo "CONGESTED ($n >= 8) — DO NOT dispatch. Exit 42; resume later."
  exit 42
fi

echo "=== [$(date -u +%FT%TZ)] leg 1: Template A full-slide comparison ==="
cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 1700 python3 $PY comparison \
  "$Q/render_4.png" \
  "$DECK/unique_slides/slide_014.jpg" \
  --view "Slide 014 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$Q/judge_attempt_4.txt" \
  -p "$(cat "$Q/payload_A_4.txt")"
echo "Template A exit=$?"

echo "=== [$(date -u +%FT%TZ)] leg 2: Procedure B — 3 crop pairs ==="
declare -A DESCS=(
  [bands]="the two full-width navy-ruled bands (ridge-regularization band and objective-function band)"
  [vectors]="the two maroon-bordered vector-definition boxes (y and y-hat stacked-vector equations)"
  [final]="the final pale-cyan full-width band with the boxed objective function"
)
for NAME in bands vectors final; do
  n2=$(pgrep -c -f analyze_image.py || true)
  echo "--- crop pair $NAME (congestion now $n2) ---"
  if [ "$n2" -ge 8 ]; then
    echo "CONGESTED before crop $NAME — stop leg 2 here; resume with this loop later."
    exit 42
  fi
  cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 1700 python3 $PY comparison \
    "$Q/crop_4_${NAME}_render.png" \
    "$Q/crop_4_${NAME}_orig.png" \
    --view "Slide 014 zoomed crop ${NAME} — render vs original at matched scale (attempt 4)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESCS[$NAME]}" \
    --thinking high --max-tokens 65536 \
    --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$Q/crop_4_${NAME}_judge.txt" \
    -p "$(cat "$Q/payload_B_4.txt")"
  echo "crop $NAME exit=$?"
done

echo "=== [$(date -u +%FT%TZ)] all legs dispatched.  Read each transcript for a real 'FINAL VERDICT:' line. ==="
