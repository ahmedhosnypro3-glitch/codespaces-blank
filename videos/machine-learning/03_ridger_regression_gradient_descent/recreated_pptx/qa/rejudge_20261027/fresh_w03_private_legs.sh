#!/usr/bin/env bash
# fresh_w03_private_legs.sh — W03-private rejudge legs writing to *_w03.txt
# transcripts that no foreign carrier touches (storm-proof evidence).
# usage: bash fresh_w03_private_legs.sh   (launches the 7 still-missing W03 legs)
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/fresh_w03_legs.log
mkdir -p "$RJ/legs_20261031.pids"

plaunch_full() { # N
  local N=$1
  local D=$RJ/slide$N NN=$((10#$N))
  nohup bash "$RJ/vision_leg.sh" "$D/judge_full_w03.txt" 1200 "$D/render.png" "$NS/unique_slides/slide_$N.jpg" \
    "Slide $NN recreation — fidelity check vs original lecture frame" \
    "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
    "$RJ/payload_A.txt" > "$D/judge_full_w03.wrapper.out" 2>&1 &
  echo $! > "$RJ/legs_20261031.pids/${N}_full_w03.pid"
  echo "$(date -u +%FT%TZ) LAUNCH-W03 $N full -> judge_full_w03.txt pid=$!" >> "$LOG"
}
plaunch_crop() { # N
  local N=$1
  local D=$RJ/slide$N NN=$((10#$N)) T R
  [ -f "$RJ/payload_B_$N.txt" ] || sed "s/slide NNN/slide $N/g" "$RJ/payload_B.tmpl" > "$RJ/payload_B_$N.txt"
  T=$(sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=$NN;" 2>/dev/null | head -1); [ -n "$T" ] || T="slide $NN"
  R=$(python3 "$RJ/pick_dense_region.py" "$N" 2>/dev/null | awk '{printf "%s,%s-%s,%s", $1,$2,$3,$4}')
  nohup bash "$RJ/vision_leg.sh" "$D/crop_dense_judge_w03.txt" 600 "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
    "Slide $NN zoomed crop dense — render vs original at matched scale (rejudge 1)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $NN (frame px $R) — $T" \
    "$RJ/payload_B_$N.txt" > "$D/crop_dense_judge_w03.wrapper.out" 2>&1 &
  echo $! > "$RJ/legs_20261031.pids/${N}_crop_w03.pid"
  echo "$(date -u +%FT%TZ) LAUNCH-W03 $N crop -> crop_dense_judge_w03.txt pid=$! region=$R" >> "$LOG"
}

plaunch_crop 030; sleep 10
plaunch_full 032; sleep 10; plaunch_crop 032; sleep 10
plaunch_full 033; sleep 10
plaunch_full 034; sleep 10; plaunch_crop 034
echo "$(date -u +%FT%TZ) W03 private batch done" >> "$LOG"
