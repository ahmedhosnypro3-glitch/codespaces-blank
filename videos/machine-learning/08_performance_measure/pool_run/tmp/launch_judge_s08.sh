#!/usr/bin/env bash
# launch_judge_s08.sh <render.png> <out_transcript.txt> — poll gate slots; the
# instant one is free, launch the mandated original-first judge through
# scripts/16_vision_gate.sh so the 540s wall is spent on the vision call.
set -u
REPO=/home/codespace/ai_llm_slides
NS=$REPO/videos/machine-learning/08_performance_measure
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
RENDER="$1"
OUT="$2"
POLL_DEADLINE=$((SECONDS + 2400))
while [ $SECONDS -lt $POLL_DEADLINE ]; do
  launched=0
  for i in $(seq 0 15); do
    f="${TMPDIR:-/tmp}/ir_vision_gate_$i.lock"
    if flock -n -w 0 "$f" true 2>/dev/null; then
      launched=1
      break
    fi
  done
  if [ $launched -eq 1 ]; then
    echo "free slot observed at $(date +%T); launching gate for $OUT"
    timeout 540 bash "$REPO/scripts/16_vision_gate.sh" "$PY" \
      "$REPO/.agents/skills/image-analysis/scripts/analyze_image.py" comparison \
      "$NS/unique_slides/slide_008.jpg" "$RENDER" \
      --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
      -p "$(cat "$NS/pool_run/judge_prompt_template.txt")" > "$OUT" 2>&1
    rc=$?
    echo "rc=$rc at $(date +%T)" >> "$OUT"
    echo "launched-and-finished rc=$rc verdicts=$(grep -c 'FINAL VERDICT' "$OUT")"
    exit $rc
  fi
  sleep 2
done
echo "no free slot within poll deadline at $(date +%T)"
exit 42
