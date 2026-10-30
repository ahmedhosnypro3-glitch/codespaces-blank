#!/usr/bin/env bash
# Slide 019 — attempt 7 judge-leg dispatches (Template A + Procedure B crops).
# Payloads are byte-verified against shared_patterns/judge_protocol_03.md.
# Run when the gateway fleet has drained: pgrep -c -f analyze_image.py should be < 8.
set -eu
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
cd /workspaces/codespaces-blank/ai_llm_slides
VID=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$VID/recreated_pptx/qa/slide019

# ── Leg 1: Template A (full-slide) ──────────────────────────────────────────
scripts/16_vision_gate.sh timeout 2400 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_7.png $VID/unique_slides/slide_019.jpg \
  --view "Slide 019 recreation attempt 7 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_7.txt \
  -p "$(cat scratch/tmp/judgeA7_payload.txt)"

# ── Leg 2: Procedure B crop certificates (re-cut from render_7) ─────────────
for NAME in noreg_rows table_right table_left; do
  scripts/16_vision_gate.sh timeout 2400 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/crop_7_${NAME}_render.png $Q/crop_7_${NAME}_orig.png \
    --view "Slide 019 zoomed crop ${NAME} — render vs original at matched scale (attempt 7)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: see worker_report.md Procedure B table" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    --transcript $Q/crop_7_${NAME}_judge.txt \
    -p "$(cat scratch/tmp/judgeB7_payload.txt)"
done
