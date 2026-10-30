#!/bin/bash
# Slide 015 — attempt-6 Procedure B crop-pair judge (Template B), one region per call:
#   dispatch_6_crop.sh <eq_stack|pinkbox|peachbox|deriv_stack|solution>
# Payload sourced fresh from the frozen template shared_patterns/judge_protocol_03.md
# (Template B); only legal substitution slide NNN -> slide 015, md5-checked in-run.
# Crops cut from render_6 by cut_crops_6.py at matched effective scale (crops_6.json).
cd /home/ahmed/Projects/ai_llm_slides || exit 9
NAME="${1:?usage: dispatch_6_crop.sh <eq_stack|pinkbox|peachbox|deriv_stack|solution>}"
DECK=videos/machine-learning/03_ridger_regression_gradient_descent
case "$NAME" in
  eq_stack)    REGION="three-line J(W) objective-function expansion stack in the cream rect (each line ends with an inline green +1/2 lambda W-transpose-W term)" ;;
  pinkbox)     REGION="the red-bordered callout box: dJ/dW = 0 identity and the 'Get Best W that minimizes the Objective Function J(W)' sentence (the W of Best W is red in the original)" ;;
  peachbox)    REGION="the peach Remember box: red bold 'Remember' label and the dW-transpose-W/dW = 2W identity with green W" ;;
  deriv_stack) REGION="the two dJ/dW gradient simplification lines ending in +lambda W and +lambda I W" ;;
  solution)    REGION="the green result box with the closed-form W = (X-transpose-X + lambda I)^-1 X-transpose-Y solution" ;;
  *) echo "unknown region $NAME"; exit 2 ;;
esac

PAYLOAD=$(python3 - <<'PY'
import hashlib
p = "videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md"
txt = open(p, encoding="utf-8").read()
sec = txt.split("## Template B")[1]
line = [l for l in sec.splitlines() if l.lstrip().startswith('-p "GROUND RULES')]
assert len(line) == 1, f"expected 1 payload line, got {len(line)}"
payload = line[0].strip()[len('-p "'):].rstrip()
assert payload.endswith('"'), "payload does not end with quote"
payload = payload[:-1].replace("slide NNN", "slide 015")
assert "NNN" not in payload
h = hashlib.md5(payload.encode()).hexdigest()
print(payload)
import sys
print(f"payload_md5={h} chars={len(payload)}", file=sys.stderr)
assert h == "978be75de7b83501d09f8f0c5576cbee", f"payload md5 mismatch: {h}"
PY
) || { echo "PAYLOAD EXTRACTION FAILED"; exit 8; }

LOAD=$(pgrep -c -f analyze_image.py); echo "gate load: $LOAD"
[ "$LOAD" -lt 8 ] || { echo "GATE CLOSED"; exit 7; }

scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $DECK/recreated_pptx/qa/slide_015/crop_6_${NAME}_render.png \
  $DECK/recreated_pptx/qa/slide_015/crop_6_${NAME}_orig.png \
  --view "Slide 015 zoomed crop ${NAME} — render vs original at matched scale (attempt 6)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${REGION}" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript $DECK/recreated_pptx/qa/slide_015/crop_6_${NAME}_judge.txt \
  -p "$PAYLOAD"
echo "CROP $NAME DONE rc=$?"
