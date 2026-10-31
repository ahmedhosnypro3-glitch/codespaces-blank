#!/usr/bin/env bash
# launch_judge_s08_r3.sh — poll gate slots; the instant one is free, launch the
# mandated judge command through scripts/16_vision_gate.sh (which re-locks a
# slot itself) so the 540s wall is spent on the vision call, not on queueing.
set -u
REPO=/home/codespace/ai_llm_slides
NS=$REPO/videos/machine-learning/08_performance_measure
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
OUT="$NS/recreated_pptx/qa/slide008/judge_attempt_2_r3.txt"
POLL_DEADLINE=$((SECONDS + 1500))
launched=0
while [ $SECONDS -lt $POLL_DEADLINE ]; do
  for i in $(seq 0 15); do
    f="${TMPDIR:-/tmp}/ir_vision_gate_$i.lock"
    if flock -n -w 0 "$f" true 2>/dev/null; then
      launched=1
      break
    fi
  done
  if [ $launched -eq 1 ]; then
    echo "free slot observed at $(date +%T); launching gate"
    timeout 540 bash "$REPO/scripts/16_vision_gate.sh" "$PY" \
      "$REPO/.agents/skills/image-analysis/scripts/analyze_image.py" comparison \
      "$NS/unique_slides/slide_008.jpg" "$NS/recreated_pptx/qa/slide008/render_3.png" \
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
