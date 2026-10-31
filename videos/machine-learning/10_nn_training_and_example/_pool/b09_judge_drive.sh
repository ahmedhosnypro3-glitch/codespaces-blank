#!/usr/bin/env bash
# b09 judge driver — storm clause: on Connection error / 429 / 502 / 504 / abort,
# sleep 120s and retry (widen wall per W4 doctrine) up to $6 attempts.
S="$1"      # slide id e.g. 017
R="$2"      # render png (image 1)
A="$3"      # first attempt number
MAX="$4"    # total attempts
T1="$5"     # wall for first try
T2="$6"     # wall for retries
TPL=judge_template.txt
OUT="qa/slide${S}/rejudge/judge_attempt_"
GATE=_pool/vision_gate.sh
PY=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
for ((i = A; i < A + MAX; i++)); do
  TO="$T1"; [ "$i" -gt "$A" ] && TO="$T2"
  echo "[$(date +%H:%M:%S)] attempt $i wall=$TO" >&2
  env VISION_SLOTS=3 timeout $((TO + 60)) bash "$GATE" python3 "$PY" \
    comparison "$R" "unique_slides/slide_${S}.jpg" \
    --timeout "$TO" --rounds 1 --tries 1 \
    -p "$(cat "$TPL")" > "${OUT}${i}.txt" 2>&1
  if grep -q "FINAL VERDICT" "${OUT}${i}.txt" 2>/dev/null; then
    echo "[$(date +%H:%M:%S)] verdict landed: $(grep 'FINAL VERDICT' "${OUT}${i}.txt" | tail -1)" >&2
    exit 0
  fi
  echo "[$(date +%H:%M:%S)] no verdict (storm/wall) — sleeping 120" >&2
  sleep 120
done
echo "[$(date +%H:%M:%S)] exhausted attempts" >&2
exit 3
