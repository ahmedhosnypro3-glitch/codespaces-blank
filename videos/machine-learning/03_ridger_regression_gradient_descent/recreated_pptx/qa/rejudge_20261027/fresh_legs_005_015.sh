#!/usr/bin/env bash
# fresh_legs_005_015.sh — launch the remaining fresh rejudge legs for the open
# slides 001-017 sweep (per-leg live check): 005 full, 012 crop, 013 crop,
# 014 full, 015 crop. 003 crop is owned by fresh_worker_001_017.sh pass 2.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp; mkdir -p "$TMPDIR"
LOG=$RJ/driver_fresh_legs_005_015.log
exec >> "$LOG" 2>&1
echo "=== fresh_legs_005_015 start $(date -u +%FT%TZ) pid=$$"
live() { if [ "$2" = full ]; then pgrep -af 'vision_leg[.]sh' | grep "slide$1/" | grep -q 'judge_full'; else pgrep -af 'vision_leg[.]sh' | grep "slide$1/" | grep -q 'crop_dense'; fi; }
title_of() { grep -m1 "^TITLE=" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2-; }
region_of() { grep -m1 "^REGION=" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2-; }
declare -a JP=() JN=()
for item in "005:full" "012:crop" "013:crop" "014:full" "015:crop"; do
  N=${item%%:*}; L=${item##*:}; D=$RJ/slide$N; NN=$((10#$N))
  if live "$N" "$L"; then echo "SKIP $N $L live wrapper on same leg"; continue; fi
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"; R=$(region_of "$N"); [ -n "$R" ] || R="?"
  if [ "$L" = full ]; then
    OUT=$D/judge_full_fresh2.txt; TMO=1200; I1=$D/render.png; I2=$ROOT/$NS/unique_slides/slide_$N.jpg
    V="Slide $NN recreation — fidelity check vs original lecture frame"
    C="IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original lecture video frame"
    P=$RJ/payload_A.txt
  else
    OUT=$D/crop_dense_judge_fresh2.txt; TMO=600; I1=$D/crop_dense_render.png; I2=$D/crop_dense_orig.png
    V="Slide $NN zoomed crop — fidelity check vs original (fresh leg)"
    C="IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame (region $R) — $T"
    P=$RJ/payload_B_$N.txt
    [ -f "$P" ] || sed "s/slide NNN/slide $N/g" "$RJ/payload_B.tmpl" > "$P"
  fi
  OCC_MAX=1000 nohup bash "$RJ/vision_leg.sh" "$OUT" "$TMO" "$I1" "$I2" "$V" "$C" "$P" >> "$RJ/leg_${N}_${L}_fresh2.log" 2>&1 &
  JP+=($!); JN+=("$N:$L"); echo "LAUNCH $N $L pid=$! out=$(basename "$OUT") $(date -u +%FT%TZ)"; sleep 15
done
for i in "${!JP[@]}"; do wait "${JP[$i]}"; echo "LEG_DONE ${JN[$i]} rc=$? $(date -u +%FT%TZ)"; done
echo "=== fresh_legs_005_015 DONE $(date -u +%FT%TZ)"
