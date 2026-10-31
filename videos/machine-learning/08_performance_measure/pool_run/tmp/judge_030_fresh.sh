#!/usr/bin/env bash
# Judge slide 30 (fresh rebuild) with 429-retry loop. Original FIRST, render SECOND.
# Usage: judge_030_fresh.sh <attempt_K> <render_png_basename> [outfile_suffix]
# Waits for a free vision-gate slot before each try so the 540s wall is spent
# streaming, not queueing behind the saturated fleet.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/08_performance_measure
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
K=${1:?attempt number}
RENDER=${2:-render_3.png}
TAG=${3:-}
OUT=$NS/recreated_pptx/qa/slide030
ORIG=$NS/unique_slides/slide_030.jpg
REN=$OUT/$RENDER
PROMPT=$(cat $NS/pool_run/judge_prompt_template.txt)
DEST=$OUT/judge_attempt_${K}${TAG}.txt

wait_slot() {
  for i in $(seq 0 15); do
    if flock -n 9>>/tmp/ir_vision_gate_$i.lock 2>/dev/null; then
      flock -u 9 9>&-
      return 0
    fi
  done
  return 1
}

cd $ROOT
for i in $(seq 1 8); do
  # wait until a gate slot is free (poll every 20s, no timeout)
  while ! wait_slot; do sleep 20; done
  echo "=== ${DEST##*/} try $i $(date -u +%H:%M:%S) (slot free) ==="
  timeout 540 bash scripts/16_vision_gate.sh "$PY" .agents/skills/image-analysis/scripts/analyze_image.py \
    comparison "$ORIG" "$REN" \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$DEST" 2>&1
  rc=$?
  echo "rc=$rc"
  if grep -q "FINAL VERDICT" "$DEST"; then
    echo "verdict reached on try $i"
    break
  fi
  if grep -q "HTTP 429" "$DEST"; then
    echo "429 seen -> sleep 300"
    sleep 300
    continue
  fi
  if grep -q "HTTP 400" "$DEST"; then
    echo "400 seen -> payload bug, aborting retries"
    break
  fi
  echo "no verdict (rc=$rc) -> sleep 180"
  sleep 180
done
echo "=== done ==="
grep -E "FINAL VERDICT|HTTP 429|HTTP 400" "$DEST" | tail -5
