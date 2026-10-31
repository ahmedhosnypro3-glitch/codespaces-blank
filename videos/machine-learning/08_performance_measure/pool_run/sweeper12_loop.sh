#!/usr/bin/env bash
# Certify-and-merge sweeper loop. From namespace root:
#   bash pool_run/sweeper12_loop.sh
# Scans for dual-PASS uncertified slides, flock-appends a ledger row, runs the
# merge update, marks the mission.db scope done, sleeps 60s, rescans.
# Exits 0 when 37/37 certified.
set -u
cd "$(dirname "$0")/.."
LOG=pool_run/sweeper12.log
echo "$(date -Is) sweeper12 loop start" >> "$LOG"
while true; do
    out=$(python3 pool_run/sweeper12_scan.py 2>>"$LOG")
    cert_count=$(echo "$out" | sed -n 's/^CERTIFIED \([0-9]*\)\/37/\1/p')
    echo "$(date -Is) scan: certified=${cert_count:-?}/37" >> "$LOG"
    if [ "${cert_count:-0}" = "37" ]; then
        echo "$(date -Is) 37/37 certified — sweeper exit" >> "$LOG"
        exit 0
    fi
    progress=0
    while read -r _ n att ver; do
        [ "${_:-}" = "DUAL" ] || continue
        nnn=$(printf '%03d' "$n")
        echo "$(date -Is) certifying slide $n attempt=$att verify=$ver" >> "$LOG"
        (
            flock -x 200
            printf '| %s | %s | %s | PASS / PASS (original-first dual-read) | analysis/reanalysis/slide_%03d_raw.json | certified=yes | sweeper12 %s |\n' \
                "$n" "$att" "$ver" "$n" "$(date -Is)" >> pool_run/verification_ledger.md
        ) 200>pool_run/verification_ledger.md.lock
        python3 pool_run/merge_final_deck.py update "$n" "recreated_pptx/slide_${nnn}_recreated.pptx" 08-performance_final.pptx >> "$LOG" 2>&1
        for i in 1 2 3 4 5; do
            if sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-$n';" 2>>"$LOG"; then
                break
            fi
            sleep 5
        done
        progress=1
    done <<< "$out"
    if [ "$progress" = "0" ]; then
        sleep 60
    else
        sleep 60
    fi
done
