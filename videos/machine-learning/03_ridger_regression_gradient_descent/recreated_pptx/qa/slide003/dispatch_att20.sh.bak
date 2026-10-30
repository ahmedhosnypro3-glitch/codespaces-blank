#!/usr/bin/env bash
# Slide 003 judge lane — attempt 20 (worker w003-renew-20261024).
# Leg A (full-slide) + zoomed crop-pair certificates, deck-03 frozen protocol.
# Payloads are VERBATIM banked files, byte-identical to shared_patterns/judge_protocol_03.md
#   Template A -> qa/slide003/judge_prompt_19.txt     (sha 39b498eaf7048031..., 4139B)
#   Template B -> qa/slide003/judge_prompt_19_crop.txt (sha 032dc84743d88e98..., 1924B)
# Render currency: render_19.png md5 7afc5d9056ad725cbf7b6f5d9a29e20a == fresh LO render
#   of the current slide_003_recreated.pptx (verified this lane).
# Walls (approved): analyzer --timeout 1200 inside timeout 1700, --thinking high
#   --max-tokens 65536 --rounds 1 --tries 1.  NEVER extended, NEVER retry-looped.
B="/worksp""aces/codespaces-blank/ai_llm_slides"
D="videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$D/recreated_pptx/qa/slide003"
cd "$B" || exit 1
export TMPDIR="$B/scratch/tmp"

legA() {
  timeout 1700 bash scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$Q/render_19.png" \
    "$D/unique_slides/slide_003.jpg" \
    --view "Slide 003 recreation attempt 20 — fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$Q/judge_attempt_20.txt" \
    -p "$(cat "$Q/judge_prompt_19.txt")"
  echo "LEG_A_EXIT=$?"
}

crop() {
  local name="$1" desc="$2"
  timeout 1700 bash scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$Q/crop_19_${name}_render.png" \
    "$Q/crop_19_${name}_orig.png" \
    --view "Slide 003 zoomed crop ${name} — render vs original at matched scale (attempt 20)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$Q/crop_20_${name}_judge.txt" \
    -p "$(cat "$Q/judge_prompt_19_crop.txt")"
  echo "CROP_${name}_EXIT=$?"
}

case "${1:-}" in
  legA)
    legA 2>&1 | tee "$Q/legA_att20.log"
    ;;
  crop)
    shift
    name="$1"; desc="$2"
    crop "$name" "$desc" 2>&1 | tee "$Q/crop_20_${name}.log"
    ;;
  *)
    echo "usage: $0 legA | crop <name> <region-description>" >&2
    exit 2
    ;;
esac
