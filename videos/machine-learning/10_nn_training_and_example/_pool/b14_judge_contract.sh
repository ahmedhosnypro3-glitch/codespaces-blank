#!/usr/bin/env bash
# b14 judge runner (contract form): comparison judge, max 6 attempts per slide.
# Storm clause: on Connection error / HTTP 429/502/504 / timeout -> sleep 120s, retry (up to 3x).
# Done only when a FINAL VERDICT: PASS transcript is banked.
# usage: b14_judge_contract.sh <N> <render.png> <outdir>
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
TOOL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS" || exit 9
N="$1"; RENDER="$2"; OUTDIR="$3"
PNN=$(printf "%03d" "$N")
mkdir -p "$OUTDIR"
LOG="$OUTDIR/judge_run.log"

verdict_ok() { [ -f "$1" ] && grep -qaE "FINAL VERDICT: ?\*{0,2}PASS" "$1"; }
storm() { grep -qaiE "HTTP (429|502|504)|Connection error|timed out|Timeout|ReadTimeout|ConnectError|every model failed" "$1"; }

a=1
stormcount=0
while [ "$a" -le 6 ]; do
  OUT="$OUTDIR/slide_${PNN}_judge_attempt${a}.txt"
  if verdict_ok "$OUT"; then
    echo "$(date '+%F %T') slide $PNN attempt $a PASS already banked" >> "$LOG"
    exit 0
  fi
  echo "$(date '+%F %T') slide $PNN attempt $a start" >> "$LOG"
  TMPDIR="$NS/_pool" timeout 400 env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 "$TOOL" comparison "unique_slides/slide_${PNN}.jpg" "$RENDER" \
    --timeout 240 --rounds 1 --tries 1 -p "$(cat "$NS/_pool/judge_template.txt")" \
    > "$OUT" 2>&1
  rc=$?
  echo "$(date '+%F %T') slide $PNN attempt $a exit=$rc bytes=$(wc -c < "$OUT")" >> "$LOG"
  if verdict_ok "$OUT"; then
    echo "$(date '+%F %T') slide $PNN attempt $a PASS BANKED" >> "$LOG"
    exit 0
  fi
  if storm "$OUT"; then
    stormcount=$((stormcount + 1))
    if [ "$stormcount" -gt 3 ]; then
      echo "$(date '+%F %T') slide $PNN provider hard-down after $stormcount storm retries" >> "$LOG"
      exit 2
    fi
    echo "$(date '+%F %T') slide $PNN storm failure, sleeping 120s (storm $stormcount)" >> "$LOG"
    sleep 120
  else
    echo "$(date '+%F %T') slide $PNN non-storm verdict: $(grep -aoE 'FINAL VERDICT: ?\*{0,2}(PASS|FAIL)' "$OUT" | tail -1)" >> "$LOG"
  fi
  a=$((a + 1))
done
echo "$(date '+%F %T') slide $PNN exhausted 6 attempts without PASS" >> "$LOG"
exit 3
