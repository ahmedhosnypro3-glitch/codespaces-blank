#!/usr/bin/env bash
# scope_a2 comparison-judge dispatcher (slides 003, 004)
# Route: DEFAULT images alias, NO --models. Wider wall per image-analysis W4
# (the 270s wall already produced a hard-wall HangError on slide 003).
# Dispatch: <=2 concurrent, ~15s spacing, ONE Bash call ending `wait`.
set -u
SKILL=/home/codespace/.agents/skills/image-analysis
VID=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
GATE=/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh
PROMPT="$(cat "$VID/judge_template.txt")"
ATT="${ATT:-2}"
cd "$SKILL" || exit 9

run_judge() {
  n="$1"
  out="$VID/recreated_pptx/qa/slide${n}/judge_attempt_${ATT}_raw.txt"
  TMPDIR=/home/codespace/ai_llm_slides/scratch/tmp timeout 540 "$GATE" \
    python3 analyze_image/analyze_image.py comparison \
    "$VID/recreated_pptx/qa/slide${n}/render-1.png" \
    "$VID/unique_slides/slide_${n}.jpg" \
    --view "Slide ${n} recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
    > "$out" 2>&1
  echo "slide ${n} judge exit=$? -> $out"
}

run_judge 003 &
sleep 15
run_judge 004 &
wait
