#!/usr/bin/env bash
# launch_014_fix2.sh — detached relaunch of slide014 fix2 judge legs.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
D=$RJ/slide014
mkdir -p "$RJ/legs_20261031.pids"

if ! pgrep -f "vision_leg.sh $D/judge_full_fix2.txt" > /dev/null; then
  OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$D/judge_full_fix2.txt" 1200 \
    "$D/render.png" "$NS/unique_slides/slide_014.jpg" \
    "Slide 14 recreation — fidelity check vs original lecture frame" \
    "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
    "$RJ/payload_A.txt" > "$D/judge_full_fix2.txt.wrapper.out" 2>&1 &
  echo $! > "$RJ/legs_20261031.pids/014_full_fix2.pid"
  echo "full fix2 launched pid $!"
else
  echo "full fix2 already running"
fi

if ! pgrep -f "vision_leg.sh $D/crop_dense_judge_fix2.txt" > /dev/null; then
  OCC_MAX=700 setsid nohup bash "$RJ/vision_leg.sh" "$D/crop_dense_judge_fix2.txt" 600 \
    "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
    "Slide 14 zoomed crop — fidelity check vs original" \
    "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
    "$RJ/payload_B_014.txt" > "$D/crop_dense_judge_fix2.txt.wrapper.out" 2>&1 &
  echo $! > "$RJ/legs_20261031.pids/014_crop_fix2.pid"
  echo "crop fix2 launched pid $!"
else
  echo "crop fix2 already running"
fi
sleep 2
pgrep -af "vision_leg.sh $D/.*fix2"
date -u +%H:%M:%S
