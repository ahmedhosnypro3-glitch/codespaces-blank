#!/usr/bin/env bash
# Verify-judge sweep: for every attempt-PASS slide lacking a verify PASS, run a
# fresh corroboration comparison (IMAGE 1 = original, IMAGE 2 = newest render)
# from the repo root, unique transcript per call. Sleeps 90-150s before each
# call; on 429 sleeps 300s and retries up to 8x. From namespace root:
#   bash pool_run/verify_sweep_r1.sh
set -u
REPO=/home/codespace/ai_llm_slides
cd "$REPO/videos/machine-learning/08_performance_measure"
LOG=pool_run/verify_sweep_r1.log
echo "$(date -Is) verify_sweep_r1 start" >> "$LOG"
while true; do
    out=$(python3 pool_run/sweeper12_scan.py 2>>"$LOG")
    cert_count=$(echo "$out" | sed -n 's/^CERTIFIED \([0-9]*\)\/37/\1/p')
    if [ "${cert_count:-0}" = "37" ]; then
        echo "$(date -Is) 37/37 — verify sweep exit" >> "$LOG"
        exit 0
    fi
    targets=$(echo "$out" | awk '$1=="NEEDVERIFY"{print $2}')
    if [ -z "$targets" ]; then
        echo "$(date -Is) no NEEDVERIFY slides; sleep 60" >> "$LOG"
        sleep 60
        continue
    fi
    for n in $targets; do
        nnn=$(printf '%03d' "$n")
        qdir="recreated_pptx/qa/slide${nnn}"
        render=$(ls -t "$qdir"/render_*.png 2>/dev/null | head -1)
        if [ -z "$render" ]; then
            echo "$(date -Is) slide $n: NO render_*.png — skip" >> "$LOG"
            continue
        fi
        t="judge_verify_sweep_$(date +%s)_s${n}.txt"
        tpath="$qdir/$t"
        s=$((90 + RANDOM % 61))
        echo "$(date -Is) slide $n: sleeping ${s}s then verify vs $render -> $tpath" >> "$LOG"
        sleep "$s"
        tries=0
        while true; do
            tries=$((tries + 1))
            ( cd "$REPO" && timeout 540 python3 .agents/skills/image-analysis/scripts/analyze_image.py \
                comparison \
                "videos/machine-learning/08_performance_measure/unique_slides/slide_${nnn}.jpg" \
                "videos/machine-learning/08_performance_measure/$render" \
                --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
                -p "$(cat "$REPO/videos/machine-learning/08_performance_measure/pool_run/judge_prompt_template.txt")" \
                > "$REPO/videos/machine-learning/08_performance_measure/$tpath" 2>&1 )
            rc=$?
            echo "exit=$rc" >> "$tpath"
            if grep -Eqi '429|rate.?limit|too many requests' "$tpath"; then
                if [ "$tries" -ge 8 ]; then
                    echo "$(date -Is) slide $n: 429 after 8 tries, giving up on this pass" >> "$LOG"
                    break
                fi
                echo "$(date -Is) slide $n: 429 detected (try $tries) — sleep 300 retry" >> "$LOG"
                sleep 300
                continue
            fi
            break
        done
        if grep -Eq 'FINAL VERDICT:\s*\*{0,2}\s*PASS' "$tpath"; then
            echo "$(date -Is) slide $n: verify PASS ($tpath)" >> "$LOG"
        else
            echo "$(date -Is) slide $n: verify NOT-PASS (rc=$rc, $tpath)" >> "$LOG"
        fi
        sleep 30
    done
    sleep 60
done
