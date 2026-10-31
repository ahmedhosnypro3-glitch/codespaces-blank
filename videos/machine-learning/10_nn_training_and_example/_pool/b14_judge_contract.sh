#!/usr/bin/env bash
# b14 judge runner (v2): comparison judge, max 6 attempts per slide.
# The namespace gate caps concurrent vision calls fleet-wide; the inner --timeout
# governs the request while the OUTER timeout must accommodate the flock queue wait.
# Storm clause: on Connection error / HTTP 429/502/504 / timeout -> sleep 120s, retry.
# Done only when a FINAL VERDICT: PASS transcript is banked.
# usage: b14_judge_contract.sh <N> <render.png> <outdir> [outer_timeout]
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
TOOL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS" || exit 9
N="$1"; RENDER="$2"; OUTDIR="$3"
OUTER="${4:-1800}"
WALL=0
if [ -n "${WALL_LIMIT:-}" ] && [ "$WALL_LIMIT" -gt 0 ] 2>/dev/null; then WALL=1; fi
PNN=$(printf "%03d" "$N")
mkdir -p "$OUTDIR"
LOG="$OUTDIR/judge_run.log"

verdict_ok() { [ -f "$1" ] && grep -qaE "FINAL VERDICT: ?\*{0,2}PASS" "$1"; }
verdict_any() { [ -f "$1" ] && grep -qaE "FINAL VERDICT: ?\*{0,2}(PASS|FAIL)" "$1"; }
storm() { grep -qaiE "HTTP (429|502|504)|Connection error|timed out|Timeout|ReadTimeout|ConnectError|every model failed" "$1"; }

a=1
stormcount=0
while [ "$a" -le 6 ]; do
  OUT="$OUTDIR/slide_${PNN}_judge_attempt${a}.txt"
  if verdict_ok "$OUT"; then
    echo "$(date '+%F %T') slide $PNN attempt $a PASS already banked" >> "$LOG"
    exit 0
  fi
  if verdict_any "$OUT"; then
    echo "$(date '+%F %T') slide $PNN attempt $a already has non-PASS verdict, skipping" >> "$LOG"
    a=$((a + 1)); continue
  fi
  echo "$(date '+%F %T') slide $PNN attempt $a start" >> "$LOG"
  TMPDIR="$NS/_pool" timeout "$OUTER" env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 "$TOOL" comparison "unique_slides/slide_${PNN}.jpg" "$RENDER" \
    --timeout 240 --rounds 1 --tries 1 -p "$(cat "$NS/_pool/judge_template.txt")" \
    > "$OUT" 2>&1
  rc=$?
  echo "$(date '+%F %T') slide $PNN attempt $a exit=$rc bytes=$(wc -c < "$OUT")" >> "$LOG"
  if verdict_ok "$OUT"; then
    echo "$(date '+%F %T') slide $PNN attempt $a PASS BANKED" >> "$LOG"
    exit 0
  fi
  if storm "$OUT" || [ "$rc" -eq 124 ] || [ "$rc" -eq 143 ]; then
    stormcount=$((stormcount + 1))
    if [ "$stormcount" -gt 3 ]; then
      echo "$(date '+%F %T') slide $PNN provider hard-down after $stormcount storm retries" >> "$LOG"
      exit 2
    fi
    echo "$(date '+%F %T') slide $PNN storm failure rc=$rc, sleeping 120s (storm $stormcount)" >> "$LOG"
    sleep 120
  else
    v=$(grep -aoE "FINAL VERDICT: ?\*{0,2}(PASS|FAIL)" "$OUT" | tail -1)
    echo "$(date '+%F %T') slide $PNN non-storm verdict: ${v:-<none>}" >> "$LOG"
  fi
  a=$((a + 1))
done
echo "$(date '+%F %T') slide $PNN exhausted 6 attempts without PASS" >> "$LOG"
exit 3
