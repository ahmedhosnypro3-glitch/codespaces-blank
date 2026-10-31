#!/bin/bash
# Doc-parse lane (this worker): slides 001..019 -> pool_run/docparse2/slideNNN/
# Max 4 concurrent per bash call (& + wait). Sleep 120s before first call.
# On timeout/429 (no parse.json with finish_reason==stop): sleep 180s, retry up to 6x.
cd /home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure || exit 1
SCRIPT=/home/codespace/.agents/skills/doc-parse/scripts/parse_document.py
OUTROOT=pool_run/docparse2
LOGS=$OUTROOT/logs
mkdir -p "$OUTROOT" "$LOGS"
RUNLOG=$LOGS/run_01_19.log
echo "$(date -Is) lane 01-19 start" >> "$RUNLOG"

sleep 120
echo "$(date -Is) initial 120s sleep done, first calls starting" >> "$RUNLOG"

ALL=$(seq -w 1 19)
declare -A ATTEMPT
for nn in $ALL; do ATTEMPT[$nn]=0; done

is_done() {
  python3 -c '
import json, glob, sys
ok = False
for p in glob.glob(sys.argv[1] + "/*.parse.json"):
    try:
        if json.load(open(p)).get("finish_reason") == "stop":
            ok = True
            break
    except Exception:
        pass
print(1 if ok else 0)
' "$OUTROOT/slide$1" 2>/dev/null || echo 0
}

run_batch() {
  local batch=("$@")
  local pids=()
  for nn in "${batch[@]}"; do
    ATTEMPT[$nn]=$(( ${ATTEMPT[$nn]} + 1 ))
    local att=${ATTEMPT[$nn]}
    local d="$OUTROOT/slide${nn}"
    rm -rf "$d"
    mkdir -p "$d"
    echo "$(date -Is) call slide${nn} attempt ${att} img=unique_slides/slide_0${nn}.jpg out=${d}" >> "$RUNLOG"
    python3 "$SCRIPT" "unique_slides/slide_0${nn}.jpg" -o "$d" --timeout 240 \
      > "$LOGS/slide${nn}_call${att}.log" 2>&1 &
    pids+=($!)
  done
  wait "${pids[@]}"
  for nn in "${batch[@]}"; do
    if [ "$(is_done "$nn")" = "1" ]; then
      echo "$(date -Is) slide${nn} DONE (attempt ${ATTEMPT[$nn]})" >> "$RUNLOG"
    else
      echo "$(date -Is) slide${nn} not-done after attempt ${ATTEMPT[$nn]}" >> "$RUNLOG"
    fi
  done
}

MAX_ATTEMPTS=7  # initial + up to 6 retries
for round in 1 2 3 4 5 6 7; do
  todo=()
  for nn in $ALL; do
    [ "$(is_done "$nn")" = "1" ] && continue
    [ "${ATTEMPT[$nn]}" -ge "$MAX_ATTEMPTS" ] && continue
    todo+=("$nn")
  done
  if [ ${#todo[@]} -eq 0 ]; then
    echo "$(date -Is) nothing left to do at round ${round}" >> "$RUNLOG"
    break
  fi
  echo "$(date -Is) round ${round}: ${#todo[@]} slides pending: ${todo[*]}" >> "$RUNLOG"
  for ((i = 0; i < ${#todo[@]}; i += 4)); do
    run_batch "${todo[@]:i:4}"
  done
  if [ "$round" -lt 7 ]; then
    echo "$(date -Is) sleeping 180s before retry round $((round + 1))" >> "$RUNLOG"
    sleep 180
  fi
done

echo "$(date -Is) final status:" >> "$RUNLOG"
ok=0
for nn in $ALL; do
  if [ "$(is_done "$nn")" = "1" ]; then
    echo "slide${nn} STOP attempts=${ATTEMPT[$nn]}" | tee -a "$RUNLOG"
    ok=$((ok + 1))
  else
    echo "slide${nn} FAILED attempts=${ATTEMPT[$nn]}" | tee -a "$RUNLOG"
  fi
done
echo "$(date -Is) lane end: ${ok}/19 banked with finish_reason=stop" >> "$RUNLOG"
echo "LANE_END ${ok}/19"
