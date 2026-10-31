#!/usr/bin/env bash
# watch_k17_poll.sh — fresh-worker poll (2026-10-31): every 3 min, up to 60 min,
# check assets_k17i2 / assets_k17j / assets_k17k for a complete 4-PNG set whose
# md5s ALL differ from assets_k15; run the composite probe for each new
# qualifying set (re-probe if the asset signature changed) and write
# slide025/pil_<set>_out.txt; append one summary line per probed set to
# watch_k17.log. Pre-existing pil files from other workers are banked as
# .pre_freshwatch.bak before overwrite (never delete evidence).
D=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025
LOG=$D/watch_k17.log
K15=$D/assets_k15
SETS="k17i2 k17j k17k"
SIG=$D/.watch_k17_poll_probed   # "set md5-of-md5s" lines for already-probed signatures
touch "$SIG"
echo "$(date -u +%FT%TZ) fresh-watch v2 start (k17a done: pil_k17a_out.txt)" >> "$LOG"
for i in $(seq 1 20); do
  for S in $SETS; do
    A=$D/assets_$S
    OUT=$D/pil_$S\_out.txt
    N=$(ls $A/plot_025_*.png 2>/dev/null | wc -l)
    CURSIG=$(ls $A/plot_025_*.png 2>/dev/null | sort | xargs md5sum 2>/dev/null | md5sum | cut -d' ' -f1)
    PROBED=$(grep "^$S " "$SIG" 2>/dev/null | cut -d' ' -f2)
    if [ "$N" -eq 4 ]; then
      QUAL=yes
      for k in tl tr bl br; do
        m1=$(md5sum $A/plot_025_$k.png 2>/dev/null | cut -d' ' -f1)
        m0=$(md5sum $K15/plot_025_$k.png 2>/dev/null | cut -d' ' -f1)
        [ -n "$m1" ] && [ "$m1" = "$m0" ] && QUAL=no
      done
      if [ "$QUAL" = yes ] && [ "$CURSIG" != "$PROBED" ]; then
        [ -f "$OUT" ] && cp -p "$OUT" "$OUT.pre_freshwatch.bak"
        python3 $D/probe_set.py "$A" "$S" "$OUT.tmp" > "$OUT.tmp" 2>&1
        mv "$OUT.tmp" "$OUT"
        SUM=$(grep '^SUMMARY:' "$OUT" | tail -1)
        echo "$(date -u +%FT%TZ) $S COMPLETE+QUALIFY (4 png, all md5!=k15) probed -> pil_${S}_out.txt | $SUM" >> "$LOG"
        grep -v "^$S " "$SIG" > "$SIG.tmp"; echo "$S $CURSIG" >> "$SIG.tmp"; mv "$SIG.tmp" "$SIG"
      elif [ "$QUAL" = no ] && [ "$CURSIG" != "$PROBED" ]; then
        echo "$(date -u +%FT%TZ) $S complete(4 png) but >=1 md5==k15; probe skipped" >> "$LOG"
        grep -v "^$S " "$SIG" > "$SIG.tmp"; echo "$S $CURSIG" >> "$SIG.tmp"; mv "$SIG.tmp" "$SIG"
      fi
    elif [ "$N" -gt 0 ] && [ "$CURSIG" != "$PROBED" ]; then
      echo "$(date -u +%FT%TZ) $S partial: $N/4 pngs" >> "$LOG"
      grep -v "^$S " "$SIG" > "$SIG.tmp"; echo "$S $CURSIG" >> "$SIG.tmp"; mv "$SIG.tmp" "$SIG"
    fi
  done
  DONE=1
  for S in $SETS; do grep -q "^$S " "$SIG" || DONE=0; done
  # end early only if all three sets reached a terminal state this watch saw
  if [ "$DONE" = 1 ] && [ $i -ge 2 ]; then echo "$(date -u +%FT%TZ) all sets reached terminal state; watch end" >> "$LOG"; exit 0; fi
  [ $i -lt 20 ] && sleep 180
done
echo "$(date -u +%FT%TZ) fresh-watch 60min timeout" >> "$LOG"
exit 1
