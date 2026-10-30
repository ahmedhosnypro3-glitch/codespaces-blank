#!/usr/bin/env bash
# Slide 014 FINAL CERTIFICATION LEGS (attempt 3) — staged, ready to fire.
# Re-check congestion IMMEDIATELY before firing: `pgrep -c -f analyze_image.py`
# must read < 8.  If it reads >= 8, run 16_vision_gate.sh's own gating: it holds
# 16 flock slots and blocks; that is the only delay the protocol allows.
#
# Payloads come from qa/slide014/payload_A_3.txt and payload_B_3.txt, banked
# byte-for-byte from shared_patterns/judge_protocol_03.md (only slide NNN -> 014;
# standalone K -> 3 with \bK\b so BLOCKER is never corrupted).  Never hand-edit
# them and never redeploy the sibling-lane banks (they were found corrupt).
#
# Legs, in order:
#   0. congestion probe  (hard gate; abort here if congested)
#   1. Template A probe  (timeout 150 / --timeout 120, opens the window)
#   2. Template A judge  (the full-slide comparison)
#   3. Procedure B       (4 zoomed crop pairs at matched effective scale 2.0847)
#
# Walls: outer `timeout 1700` > gate internal ladder > per-call --timeout 600.
# ONE hard-wall retry per leg (W4) is protocol; never add other retry loops.
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$DECK/recreated_pptx/qa/slide014"
PY=".agents/skills/image-analysis/scripts/analyze_image.py"
export TMPDIR="$ROOT/scratch/tmp"
mkdir -p "$TMPDIR"

echo "=== [$(date -u +%FT%TZ)] leg 0: congestion probe ==="
n=$(pgrep -c -f analyze_image.py || true)
echo "analyze_image.py processes: $n"
if [ "$n" -ge 8 ]; then
  echo "CONGESTED ($n >= 8) — DO NOT dispatch. Sleep 240 and re-probe."
  exit 42
fi

echo "=== [$(date -u +%FT%TZ)] leg 1: Template A probe ==="
cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 150 python3 $PY analysis \
  "$Q/render_3.png" \
  --view "Slide 014 recreation attempt 3 — probe" \
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
  --timeout 120 --rounds 1 --tries 1 \
  --transcript "$Q/probe_3.txt"
echo "probe exit=$? (0 = window open)"

echo "=== [$(date -u +%FT%TZ)] leg 2: Template A full-slide comparison ==="
cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 1700 python3 $PY comparison \
  "$Q/render_3.png" \
  "$DECK/unique_slides/slide_014.jpg" \
  --view "Slide 014 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/judge_attempt_3.txt" \
  -p "$(cat "$Q/payload_A_3.txt")"
echo "Template A exit=$?"

echo "=== [$(date -u +%FT%TZ)] leg 3: Procedure B — 4 crop pairs ==="
declare -A DESCS=(
  [title_boxes]="title band and the two vector-definition boxes (Original / Predicted Labels)"
  [upper_bands]="ridge-regularization and objective-function full-width bands"
  [middle_bands]="the stacked peach and yellow bands in the middle region, with the centre gutter"
  [lower_region]="loss-term and regularization-term boxes with the final objective-function band"
)
for NAME in title_boxes upper_bands middle_bands lower_region; do
  n2=$(pgrep -c -f analyze_image.py || true)
  echo "--- crop pair $NAME (congestion now $n2) ---"
  if [ "$n2" -ge 8 ]; then
    echo "CONGESTED before crop $NAME — stop leg 3 here; resume with this loop later."
    exit 42
  fi
  cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 1700 python3 $PY comparison \
    "$Q/crop_3_${NAME}_render.png" \
    "$Q/crop_3_${NAME}_orig.png" \
    --view "Slide 014 zoomed crop ${NAME} — render vs original at matched scale (attempt 3)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESCS[$NAME]}" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript "$Q/crop_3_${NAME}_judge.txt" \
    -p "$(cat "$Q/payload_B_3.txt")"
  echo "crop $NAME exit=$?"
done

echo "=== [$(date -u +%FT%TZ)] all legs dispatched.  Read each transcript for a real 'FINAL VERDICT:' line. ==="
