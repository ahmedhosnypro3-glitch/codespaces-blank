#!/bin/bash
# Sweeper #3: certify+merge loop. Scans for dual-PASS uncertified slides,
# appends verification_ledger.md row under flock, merges into final deck,
# marks scope done in mission.db (sleep 5 on lock). Never rebuilds/re-judges.
set -u
cd /home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
ITER=${1:-6}
SLEEP=${2:-45}
LOG=pool_run/sweeper3.log

for i in $(seq 1 "$ITER"); do
  echo "[$(date -u +%H:%M:%S)] iteration $i scan" >> "$LOG"
  while IFS=$'\t' read -r n att ver; do
    [ -z "$n" ] && continue
    dir=$(printf 'slide%03d' "$n")
    pptx="recreated_pptx/slide_${dir#slide}_recreated.pptx"
    pptx=$(printf 'recreated_pptx/slide_%03d_recreated.pptx' "$n")
    if [ ! -f "$pptx" ]; then
      echo "[$(date -u +%H:%M:%S)] slide $n: pptx missing ($pptx), skip" >> "$LOG"
      continue
    fi
    # skip if another sweeper already certified it in the deck ledger
    cert=$(python3 -c "
import json
d=json.load(open('final_deck_ledger.json'))
print('yes' if any(p['slide_num']==$n and p['status']=='certified' for p in d['pages']) else 'no')")
    if [ "$cert" = "yes" ]; then
      echo "[$(date -u +%H:%M:%S)] slide $n already certified, skip" >> "$LOG"
      continue
    fi
    row="| $n | $att | $ver | PASS/PASS (original-first) | analysis/reanalysis/slide_$(printf '%03d' "$n")_raw.json | certified=yes |"
    ( flock -x 9; printf '%s\n' "$row" >> pool_run/verification_ledger.md ) 9>pool_run/.verification_ledger.lock
    echo "[$(date -u +%H:%M:%S)] slide $n ledger row appended: $row" >> "$LOG"
    if python3 pool_run/merge_final_deck.py update "$n" "$pptx" 08-performance_final.pptx >> "$LOG" 2>&1; then
      echo "[$(date -u +%H:%M:%S)] slide $n merged into 08-performance_final.pptx page $n" >> "$LOG"
    else
      echo "[$(date -u +%H:%M:%S)] slide $n MERGE FAILED" >> "$LOG"
      continue
    fi
    for try in 1 2 3 4 5 6; do
      if sqlite3 pool_run/mission.db "UPDATE scopes SET status='done', agent=COALESCE(agent,'sweeper-3'), note='sweeper-3 certified+merged: dual-PASS original-first ($att + $ver), ledger row appended, merged to final deck page $n', updated_at=datetime('now') WHERE name='slide-$n';" 2>>"$LOG"; then
        echo "[$(date -u +%H:%M:%S)] slide $n scope slide-$n marked done" >> "$LOG"
        break
      else
        echo "[$(date -u +%H:%M:%S)] slide $n db lock, sleep 5 (try $try)" >> "$LOG"
        sleep 5
      fi
    done
  done < <(python3 pool_run/sweeper3_scan.py)
  sleep "$SLEEP"
done
echo "[$(date -u +%H:%M:%S)] loop finished" >> "$LOG"
