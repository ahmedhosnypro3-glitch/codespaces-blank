#!/usr/bin/env bash
# launch_leg.sh NNN full|crop
set -u
N=$1; leg=$2
ROOT=/home/codespace/ai_llm_slides
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
D=$RJ/slide$N
NN=$((10#$N))
if [ "$leg" = full ]; then
  if [ -f "$D/judge_full.txt" ]; then FT=judge_full_fresh.txt; else FT=judge_full.txt; fi
  T=$D/$FT; TMO=1200; IMG1=$D/render.png; IMG2=$NS/unique_slides/slide_$N.jpg; PAY=$RJ/payload_A.txt
  VIEW="Slide $NN recreation — fidelity check vs original lecture frame"
  CAP="IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame"
else
  if [ -f "$D/crop_dense_judge.txt" ]; then CT=crop_dense_judge_fresh.txt; else CT=crop_dense_judge.txt; fi
  T=$D/$CT; TMO=600; IMG1=$D/crop_dense_render.png; IMG2=$D/crop_dense_orig.png; PAY=$RJ/payload_B_$N.txt
  VIEW="Slide $NN zoomed crop — fidelity check vs original"
  CAP="IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame"
fi
[ -f "$PAY" ] || sed "s/slide NNN/slide $N/g" "$RJ/payload_B.tmpl" > "$PAY"
setsid nohup bash "$RJ/vision_leg.sh" "$T" "$TMO" "$IMG1" "$IMG2" "$VIEW" "$CAP" "$PAY" > "$T.wrapper.out" 2>&1 &
echo $! > "$RJ/legs_20261031.pids/${N}_${leg}.pid"
echo "launched $N $leg -> $T pid $!"
