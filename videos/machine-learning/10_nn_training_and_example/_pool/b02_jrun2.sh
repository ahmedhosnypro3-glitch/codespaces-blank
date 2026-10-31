#!/usr/bin/env bash
# b02 judge runner: per-slide retries (storm clause: 120s sleep, 3 tries),
# wide wall (outer 1500 / inner 420), transcripts banked per attempt.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
PROMPT="$(cat judge_template.txt)"
run_one() {
  local n="$1"
  for k in 1 2 3; do
    local out="qa/slide${n}/rejudge/r2/judge_attempt_${k}.txt"
    [ -s "$out" ] && grep -q 'FINAL VERDICT' "$out" && { echo "slide $n attempt $k already has verdict" >> _pool/b02_jrun2.out; return 0; }
    timeout 1500 ./_pool/vision_gate.sh timeout 540 \
      python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
      comparison "qa/slide${n}/rejudge/r2/render-1.png" "unique_slides/slide_${n}.jpg" \
      --view "Slide ${n} recreation render vs original lecture frame" \
      --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
      -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$out" 2>&1
    echo "slide ${n} attempt ${k} rc=$? $(date -u +%T) bytes=$(wc -c < "$out")" >> _pool/b02_jrun2.out
    grep -q 'FINAL VERDICT' "$out" && { echo "slide ${n} attempt ${k} VERDICT" >> _pool/b02_jrun2.out; return 0; }
    sleep 120
  done
  echo "slide ${n} exhausted 3 attempts" >> _pool/b02_jrun2.out
}
run_one 003 &
P1=$!
sleep 15
run_one 004 &
P2=$!
wait $P1 $P2
echo "both runners done $(date -u +%T)" >> _pool/b02_jrun2.out
