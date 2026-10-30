#!/usr/bin/env bash
# scope_r1 comparison-judge dispatcher (REJUDGE_PROTOCOL step 4)
# usage: r1_judge.sh <NNN>   e.g. 001
set -u
N="$1"
VD=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SK=/home/codespace/.agents/skills/image-analysis
GATE=/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh
OUT="$VD/qa/slide${N}/rejudge/judge_attempt_${R1_ATTEMPT:-1}.txt"
cd "$SK" || exit 9
PROMPT="$(cat "$VD/judge_template.txt")"
# Inner 600s (the tool's native default) / outer 1200s: the 16-slot vision gate's
# flock wait happens INSIDE the outer timeout, and the tool's hard wall is
# inner+30s, so both must clear the comparison payload of two images in one request.
TMPDIR="$VD/_pool" timeout "${R1_OUTER:-1200}" "$GATE" python3 analyze_image/analyze_image.py comparison \
  "$VD/qa/slide${N}/rejudge/render-1.png" \
  "$VD/unique_slides/slide_${N}.jpg" \
  --view "Slide ${N} recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout "${R1_INNER:-600}" --rounds 1 --tries 1 \
  > "$OUT" 2>&1
rc=$?
echo "slide${N} judge exit=$rc -> $OUT"
exit 0
