#!/usr/bin/env bash
# watch_k17.sh — poll for the two parallel fix agents' k17 asset sets.
RJ=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
D=$RJ/slide025
LOG=$D/watch_k17.log
echo "watch start $(date -u +%FT%TZ)" > "$LOG"
for i in $(seq 1 95); do
  sleep 60
  A=""; B=""
  for f in assets_k17a/plot_025_tl.png assets_k17a/plot_025_tr.png assets_k17a/plot_025_bl.png assets_k17a/plot_025_br.png assets_k17a/pil_k17a_out.txt; do
    [ -f "$D/$f" ] && A="$A $(basename $f):$(stat -c %s $D/$f)"
  done
  for f in assets_k17b2/plot_025_tl.png assets_k17b2/plot_025_tr.png assets_k17b2/plot_025_bl.png assets_k17b2/plot_025_br.png assets_k17b2/pil_k17b_out.txt; do
    [ -f "$D/$f" ] && B="$B $(basename $f):$(stat -c %s $D/$f)"
  done
  echo "$(date -u +%FT%TZ) k17a=[${A:-none}] k17b2=[${B:-none}]" >> "$LOG"
  if [ -f "$D/assets_k17a/pil_k17a_out.txt" ] && [ -f "$D/assets_k17b2/pil_k17b_out.txt" ]; then
    echo "$(date -u +%FT%TZ) BOTH_PIL_OUT_PRESENT" >> "$LOG"; exit 0
  fi
done
echo "$(date -u +%FT%TZ) WATCH_TIMEOUT" >> "$LOG"
exit 1
