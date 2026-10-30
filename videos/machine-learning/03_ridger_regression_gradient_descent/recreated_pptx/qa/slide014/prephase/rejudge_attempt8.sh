#!/usr/bin/env bash
# Slide 014 STAGED re-judge dispatcher (attempt 8) — S20f prephase, NOT DISPATCHED.
# Requires owner SANCTION: the 6-judge-attempt cap is exhausted (attempts 1-7;
# attempt 7 = last roll, adjudicated in qa/slide014/adjudicate_attempt_7.md).
# Render: render_7c.png = CURRENT build (S20f re-render pixel-identical, 0 diff px).
# Payloads byte-verified vs frozen shared_patterns/judge_protocol_03.md:
#   Template A = qa/slide014/payload_A_7.txt  md5 9387f5fbb94ef05a31db19f1e018dde1
#   Template B = qa/slide014/payload_B_7_<mode>.txt md5 978be75de7b83501d09f8f0c5576cbee
# (all three B files identical: crop NAME lives in --capture, not in the payload)
# Usage: rejudge_attempt8.sh <legA|vectors|bands|final>
set -u
MODE="${1:?usage: rejudge_attempt8.sh <legA|vectors|bands|final>}"
cd /home/ahmed/Projects/ai_llm_slides || exit 3
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014

# gate law: probe, yield once, then park honestly (never retry-loop)
N=$(pgrep -c -f analyze_image.py)
if [ "$N" -ge 8 ]; then sleep 240; N=$(pgrep -c -f analyze_image.py); fi
if [ "$N" -ge 8 ]; then echo "GATE CLOSED: load=$N >= 8 — PARK this leg, do not dispatch"; exit 42; fi

if [ "$MODE" = "legA" ]; then
  exec scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$Q/render_7c.png" \
    videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg \
    --view "Slide 014 recreation attempt 8 — fidelity check vs original lecture frame (owner-sanctioned re-judge)" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 \
    --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$Q/judge_attempt_8.txt" \
    -p "$(cat "$Q/payload_A_7.txt")"
fi

case "$MODE" in
  vectors) DESC="the two maroon-bordered vector-definition boxes: left 'Let Y =' + red bracketed column vector + 'Original Labels'/'from Training Samples' labels at 14pt; right 'Let Yhat =' + red bracketed column vector + 'Predicted Labels'/'from Model Yhat = XW' with the bold underlined X and W" ;;
  bands)   DESC="the two full-width pale-yellow navy-ruled bands: 'Objective is Yhat=Y and ||W|| is minimum This is called Ridge Regularization' and 'Objective function J(W) = Loss(X,Y,W) + lambda R(W) (lambda is a weighting factor)' with per-phrase red/blue/green emphasis" ;;
  final)   DESC="the bottom pale-cyan navy-ruled final band: 'Objective function' + the large 2D stacked-1/2 equation J(W) = 1/2[ (Y-Yhat)^T(Y-Yhat) + lambda W^T W ] with stacked fraction bar, superscript T and square brackets" ;;
  *) echo "unknown leg $MODE" >&2; exit 2 ;;
esac

# one-time crop re-cut from the CURRENT render (attempt-7 crops came from render_7,
# pre-fix; render_7c carries the X/label/underline fixes)
if [ ! -f "$Q/crop_8_${MODE}_render.png" ]; then
  python3 - "$Q" "$MODE" <<'EOF'
import sys
from PIL import Image
Q, mode = sys.argv[1], sys.argv[2]
DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
REGIONS = {
    "bands":   (48, 242, 910, 347),
    "vectors": (48, 50, 910, 240),
    "final":   (48, 462, 910, 532),
}
ro = Image.open(f"{DECK}/unique_slides/slide_014.jpg").convert("RGB")
rr = Image.open(f"{Q}/render_7c.png").convert("RGB")
sx, sy = rr.size[0] / ro.size[0], rr.size[1] / ro.size[1]
x0, y0, x1, y1 = REGIONS[mode]
cr = rr.crop((round(x0*sx), round(y0*sy), round(x1*sx), round(y1*sy)))
co = ro.crop((x0, y0, x1, y1)).resize(cr.size, Image.LANCZOS)
cr.save(f"{Q}/crop_8_{mode}_render.png"); co.save(f"{Q}/crop_8_{mode}_orig.png")
print(f"re-cut crop_8_{mode}: frame x{x0}..{x1} y{y0}..{y1} -> {cr.size} SCALE {sx:.4f}/{sy:.4f}")
EOF
fi

exec scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/crop_8_${MODE}_render.png" \
  "$Q/crop_8_${MODE}_orig.png" \
  --view "Slide 014 zoomed crop ${MODE} — render vs original at matched scale (attempt 8)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$Q/crop_8_${MODE}_judge.txt" \
  -p "$(cat "$Q/payload_B_7_${MODE}.txt")"
