#!/usr/bin/env bash
# b03 slide_006 fresh comparison judge on the v3 render. Storm-resilient:
# Connection error / 429 / 502 / 504 / timeout -> sleep 120s and retry (max 3 storm retries).
# Max 6 attempts total. Done only when a transcript banks FINAL VERDICT: PASS.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
TOOL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS" || exit 9
PROMPT="$(cat _pool/judge_template.txt)"
RENDER=qa/slide006/rejudge/b03/render_v3-1.png
LOG=_pool/b03_judge6.log

verdict() { grep -qaE "FINAL VERDICT: ?\*{0,2}(PASS|FAIL)" "$1" 2>/dev/null; }
storm() { grep -qaEi "connection (error|reset|aborted)|HTTP 429|HTTP 502|HTTP 504|timed out|timeout" "$1" 2>/dev/null; }

a=1
storm_retries=0
while [ "$a" -le 6 ]; do
  OUT="qa/slide006_judge_attempt${a}.txt"
  echo "$(date '+%F %T') slide006 v3 judge attempt $a start" >> "$LOG"
  env VISION_SLOTS=3 bash _pool/vision_gate.sh python3 "$TOOL" comparison \
    unique_slides/slide_006.jpg "$RENDER" --timeout 240 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$OUT" 2>&1
  rc=$?
  if verdict "$OUT"; then
    echo "$(date '+%F %T') slide006 v3 judge attempt $a VERDICT BANKED rc=$rc bytes=$(wc -c <"$OUT")" >> "$LOG"
    tail -3 "$OUT" >> "$LOG"
    exit 0
  fi
  echo "$(date '+%F %T') slide006 v3 judge attempt $a NO VERDICT rc=$rc bytes=$(wc -c <"$OUT")" >> "$LOG"
  if storm "$OUT" && [ "$storm_retries" -lt 3 ] && [ "$a" -lt 6 ]; then
    storm_retries=$((storm_retries + 1))
    echo "$(date '+%F %T') storm detected -> sleep 120 (storm_retry=$storm_retries)" >> "$LOG"
    sleep 120
  fi
  a=$((a + 1))
done
echo "$(date '+%F %T') slide006 v3 judge EXHAUSTED 6 attempts" >> "$LOG"
exit 1
