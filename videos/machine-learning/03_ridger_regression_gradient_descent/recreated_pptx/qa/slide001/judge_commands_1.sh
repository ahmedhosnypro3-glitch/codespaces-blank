#!/usr/bin/env bash
# Slide 001 attempt-1 judge dispatch set (2026-10-20, worker w4-s001-20261020T1900)
# Payloads sourced byte-for-byte from shared_patterns/judge_protocol_03.md Template A/B
# (banked as judge_prompt_1.txt / crop_prompt_1_<name>.txt by bank_prompts.py).
# Walls: per frozen protocol — gate-wrapped timeout 1700 > per-call --timeout 600,
# --thinking high --max-tokens 65536. TMPDIR pinned to project scratch so the gate
# shares the fleet-global 16-slot flock.
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide001

case "${1:-}" in
full)
  scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $QA/render_1.png \
    videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_001.jpg \
    --view "Slide 001 recreation — fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture frame" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript $QA/judge_attempt_1.txt \
    -p "$(cat $QA/judge_prompt_1.txt)"
  ;;
title|preparedby|instructors|logo)
  NAME=$1
  case "$NAME" in
    title)       DESC="three-line red title block (large bold red text)" ;;
    preparedby)  DESC="subtitle + Prepared By attribution block (small blue text)" ;;
    instructors) DESC="Instructors header + two name/email entries (left-aligned small text)" ;;
    logo)        DESC="institutional Zewail City logo (teal panel + tiny Arabic/English text)" ;;
  esac
  scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $QA/crop_1_${NAME}_render.png \
    $QA/crop_1_${NAME}_orig.png \
    --view "Slide 001 zoomed crop ${NAME} — render vs original at matched scale (attempt 1)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript $QA/crop_1_${NAME}_judge.txt \
    -p "$(cat $QA/crop_prompt_1_${NAME}.txt)"
  ;;
*) echo "usage: $0 {full|title|preparedby|instructors|logo}"; exit 2 ;;
esac
