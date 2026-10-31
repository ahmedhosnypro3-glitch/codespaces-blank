#!/usr/bin/env bash
# Sweeper #8 — certify-and-merge loop for 08_performance_measure.
# Every ~60s: scan qa dirs for dual-PASS slides not yet certified; for each,
# flock verification_ledger.md, append a PASS row (if none), run merge update,
# mark mission.db scope done, confirm ledger certification.
set -u
NS="/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
cd "$NS"
LOG="pool_run/sweeper8.log"
ITER=0

echo "$(date '+%F %T') sweeper8 start" >> "$LOG"

while true; do
  ITER=$((ITER+1))
  while IFS=$'\t' read -r n att ver; do
    [ -z "$n" ] && continue
    pptx="recreated_pptx/slide_$(printf '%03d' "$n")_recreated.pptx"
    if [ ! -f "$pptx" ]; then
      echo "$(date '+%F %T') slide $n candidate but $pptx missing — skip" >> "$LOG"
      continue
    fi
    echo "$(date '+%F %T') candidate slide $n att=$att ver=$ver" >> "$LOG"
    # 1) ledger row under flock, only if no PASS row for n yet
    flock pool_run/verification_ledger.md bash -c '
      n="$1"; att="$2"; ver="$3"; log="$4"
      if awk -v n="$n" -F"|" "\$2 ~ (\"^ *\" n \" *\$\") {v=\$5; gsub(/ /,\"\",v); if (v ~ /PASS/ && v !~ /FAIL/ && \$0 !~ /superseded/) found=1} END{exit !found}" pool_run/verification_ledger.md; then
        echo "$(date '+%F %T') slide $n already has PASS ledger row — skip" >> "$log"
      else
        printf "| %s | %s | %s | PASS / PASS (original-first dual-read; sweeper-8) | — | yes | |\n" "$n" "$att" "$ver" >> pool_run/verification_ledger.md
        echo "$(date '+%F %T') slide $n ledger row appended" >> "$log"
      fi
    ' _ "$n" "$att" "$ver" "$LOG"
    # re-check: does a PASS row now exist?
    hasrow=$(python3 - "$n" <<'PY'
import re,sys
n=sys.argv[1]
for line in open('pool_run/verification_ledger.md'):
    m=re.match(r"\|\s*(\d+)\s*\|",line)
    if m and m.group(1)==n and 'superseded' not in line:
        cols=[c.strip() for c in line.split('|')]
        v=cols[4] if len(cols)>4 else ''
        if 'PASS' in v and 'FAIL' not in v:
            print('yes'); break
PY
)
    [ "$hasrow" = "yes" ] || { echo "$(date '+%F %T') slide $n no PASS row after flock — skip merge" >> "$LOG"; continue; }
    # 2) merge update (idempotent, deck-level flock inside the script)
    sleep 5
    if python3 pool_run/merge_final_deck.py update "$n" "$pptx" 08-performance_final.pptx >> "$LOG" 2>&1; then
      echo "$(date '+%F %T') slide $n merge update OK" >> "$LOG"
    else
      echo "$(date '+%F %T') slide $n merge update FAILED rc=$?" >> "$LOG"
      continue
    fi
    # 3) mission.db scope done (retry on locked)
    for i in 1 2 3 4 5; do
      if sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-$n';" 2>>"$LOG"; then
        echo "$(date '+%F %T') slide $n scope done" >> "$LOG"
        break
      fi
      sleep 5
    done
    # 4) confirm certification in final_deck_ledger.json
    cert=$(python3 -c "
import json
d=json.load(open('final_deck_ledger.json'))
p=[x for x in d['pages'] if x['slide_num']==$n][0]
print(p['status'])")
    echo "$(date '+%F %T') slide $n ledger status=$cert" >> "$LOG"
  done < <(python3 pool_run/sweeper8_scan.py)
  sleep 60
done
