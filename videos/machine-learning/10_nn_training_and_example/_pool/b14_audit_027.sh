#!/usr/bin/env bash
# b14 wave-2 audit runner for slide 027 (analysis mode).
# Storm clause: on Connection error / HTTP 429/502/504 / timeout -> sleep 120s, retry.
# Max 3 retries before banking failure. A valid transcript has [winner] and >=4000 bytes.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
TOOL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS" || exit 9
OUT="$NS/_pool/audit2/slide_027.txt"
LOG="$NS/_pool/audit2/slide_027_run.log"
mkdir -p "$NS/_pool/audit2"

valid() { [ -f "$1" ] && grep -qa "\[winner\]" "$1" && [ "$(wc -c < "$1")" -ge 4000 ]; }
storm() { grep -qaiE "HTTP (429|502|504)|Connection error|timed out|Timeout|ReadTimeout|ConnectError" "$1"; }

r=0
while [ "$r" -le 3 ]; do
  echo "$(date '+%F %T') attempt $((r + 1)) start" >> "$LOG"
  TMPDIR="$NS/_pool" timeout 1000 bash "$NS/_pool/vision_gate.sh" \
    python3 "$TOOL" analysis "$NS/unique_slides/slide_027.jpg" \
    --timeout 900 --rounds 1 --tries 1 -p "$(cat "$NS/_pool/audit_prompt.txt")" \
    > "$OUT" 2>&1
  rc=$?
  echo "$(date '+%F %T') attempt $((r + 1)) exit=$rc bytes=$(wc -c < "$OUT")" >> "$LOG"
  if valid "$OUT"; then
    echo "$(date '+%F %T') VALID audit banked" >> "$LOG"
    exit 0
  fi
  if ! storm "$OUT"; then
    echo "$(date '+%F %T') non-storm failure - banking failure" >> "$LOG"
    exit 1
  fi
  r=$((r + 1))
  [ "$r" -le 3 ] && sleep 120
done
echo "$(date '+%F %T') provider hard-down after 3 retries" >> "$LOG"
exit 1
