#!/usr/bin/env bash
# b02 judge launcher with outer wall so a saturated gate queue cannot hang us.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
PROMPT="$(cat judge_template.txt)"
run_one() {
  local n="$1" out="$2"
  timeout 1500 ./_pool/vision_gate.sh timeout 540 \
    python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
    comparison "qa/slide${n}/rejudge/r2/render-1.png" "unique_slides/slide_${n}.jpg" \
    --view "Slide ${n} recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$out" 2>&1
  echo "slide ${n} judge rc=$? $(date -u +%T)" >> _pool/b02_jrun.out
}
run_one 003 qa/slide003/rejudge/r2/judge_attempt_1.txt &
P1=$!
sleep 15
run_one 004 qa/slide004/rejudge/r2/judge_attempt_1.txt &
P2=$!
wait $P1 $P2
echo "both done $(date -u +%T)" >> _pool/b02_jrun.out
