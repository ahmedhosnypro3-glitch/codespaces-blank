#!/bin/bash
# Lane D: doc-parse crop cascade over original frames slide_029..slide_037
# Budgets per tasking: --max-crops 16 --max-parse-calls 24.
# Backoff law: on timeout/429/5xx sleep 120-300s, retry up to 6x.
# Between slides sleep 60-90s; max 2 concurrent parse calls (--max-parallel 2).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
SKILL=~/.agents/skills/doc-parse
DP=$NS/pool_run/docparse
LOGDIR=$DP/_laneD
mkdir -p "$LOGDIR"
cd "$NS"

for N in 029 030 031 032 033 034 035 036 037; do
  OUT=$DP/slide$N
  # preserve prior banked evidence before overwriting the run dir
  if [ -d "$OUT" ]; then
    TS=$(date +%Y%m%d-%H%M%S)
    mv "$OUT" "$DP/_archive/slide${N}_laneD_${TS}"
    echo "archived previous slide$N run -> _archive/slide${N}_laneD_${TS}"
  fi
  ATTEMPT=1
  MAX_ATTEMPTS=6
  while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    echo "=== slide$N attempt $ATTEMPT $(date -Iseconds)"
    python3 "$SKILL/scripts/crop_cascade.py" "unique_slides/slide_${N}.jpg" \
      --prompt-file "$SKILL/references/prompts/crop_decision.md" \
      --out "$OUT" \
      --max-crops 16 --max-parse-calls 24 --max-depth 6 \
      --max-retries 6 --max-parallel 2 \
      --parse-timeout 150 --chat-timeout 60 \
      >> "$LOGDIR/slide${N}.cascade.log" 2>&1
    RC=$?
    echo "=== slide$N attempt $ATTEMPT rc=$RC $(date -Iseconds)"
    if [ $RC -eq 0 ]; then
      # health check: every parse.json must be finish=stop
      BAD=$(find "$OUT" -name '*.parse.json' -print0 | xargs -0 -I{} python3 -c "
import json,sys
j=json.load(open('{}'))
fr=j.get('finish_reason'); c=j.get('content') or ''
if fr!='stop' or len(c)==0: print('{}', fr, len(c))
" | head -5)
      if [ -z "$BAD" ]; then
        echo "slide$N OK (all parse calls finish=stop, non-empty)"
        break
      else
        echo "slide$N attempt $ATTEMPT produced bad parse jsons:"; echo "$BAD"
      fi
    else
      echo "slide$N attempt $ATTEMPT rc=$RC — checking log tail"
      tail -3 "$LOGDIR/slide${N}.cascade.log"
    fi
    if [ $ATTEMPT -ge $MAX_ATTEMPTS ]; then
      echo "slide$N EXHAUSTED after $MAX_ATTEMPTS attempts"
      break
    fi
    S=$((120 + RANDOM % 181))
    echo "backoff ${S}s before retry"
    sleep $S
    ATTEMPT=$((ATTEMPT + 1))
  done
  # inter-slide pacing 60-90s
  if [ "$N" != "037" ]; then
    P=$((60 + RANDOM % 31))
    echo "inter-slide pacing ${P}s"
    sleep $P
  fi
done
echo "LANE D DONE $(date -Iseconds)"
