#!/usr/bin/env bash
# Frozen-template comparison judge with the storm-resilience wide wall.
# Usage: rejudge_call.sh <slide_NNN> <attempt_tag>
# Wraps the default route (no --models) in --timeout 420 / timeout 540, which is
# the clause already banked in _pool/storm_log/STORM_RESILIENCE.log.
set -u
N="$1"
TAG="$2"
V=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
PROMPT="$(cat "$V/judge_template.txt")"
cd /home/codespace/.agents/skills/image-analysis || exit 99
timeout 540 python3 analyze_image/analyze_image.py comparison \
  "$V/qa/slide${N}/rejudge/render-1.png" "$V/unique_slides/slide_${N}.jpg" \
  --view "Slide ${N} recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 \
  > "$V/qa/slide${N}/rejudge/${TAG}.txt" 2>&1
echo "RC=$? for $N $TAG"
