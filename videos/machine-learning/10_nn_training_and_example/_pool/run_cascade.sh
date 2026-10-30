#!/usr/bin/env bash
# Doc-parse crop-cascade runner for scope_d1 (advisory lane, never gates).
# One image per invocation; fresh retry on transport-level failure.
# Run sequentially: crop_cascade's own pool keeps parse calls <=4 in flight.
set -u
VID=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/.agents/skills/doc-parse
STORM="$VID/_pool/storm_log/scope_d1.log"
SLIDE="$1"
OUT="$VID/_pool/cascade_${SLIDE}"
LOG="$VID/_pool/storm_log/cascade_${SLIDE}.log"

cd "$VID" || exit 1
for attempt in 1 2 3; do
  start=$(date -u +%H:%M:%S)
  timeout 900 python3 "$SKILL/scripts/crop_cascade.py" "unique_slides/slide_${SLIDE}.jpg" \
    --prompt-file "$SKILL/references/prompts/crop_decision.md" \
    --out "$OUT" \
    --max-crops 16 --max-parse-calls 24 --max-depth 6 --parse-timeout 180 \
    >> "$LOG" 2>&1
  rc=$?
  end=$(date -u +%H:%M:%S)
  echo "cascade_${SLIDE} attempt=${attempt} rc=${rc} ${start}->${end}" >> "$STORM"
  case "$rc" in
    0|6) exit "$rc" ;;          # complete, or partial (gaps marked in composed)
    2|3) exit "$rc" ;;          # usage / config: retry cannot help
  esac
  echo "cascade_${SLIDE} attempt=${attempt} rc=${rc}: transport/empty -> fresh retry in 60s" >> "$STORM"
  sleep 60
done
exit "$rc"
