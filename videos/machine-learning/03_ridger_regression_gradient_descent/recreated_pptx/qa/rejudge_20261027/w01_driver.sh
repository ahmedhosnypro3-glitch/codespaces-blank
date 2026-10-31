#!/usr/bin/env bash
# w01_driver.sh — fresh worker W01: fill missing rejudge legs for certified slides
# 035,036 (FULL+CROP), 037 (CROP), 041 (CROP). Prior spawns' chain (561419) covers
# 042,045,046,047,049,050,051 — not duplicated here to avoid transcript clobbering.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/driver_W01.log

leg() { # N LEG OUT TMO IMG1 IMG2 VIEW CAP PAY
  local N=$1 L=$2 OUT=$3 TMO=$4 I1=$5 I2=$6 V=$7 C=$8 P=$9
  echo "=== $N $L start $(date -u +%FT%TZ)" >> "$LOG"
  nohup bash "$RJ/vision_leg.sh" "$OUT" "$TMO" "$I1" "$I2" "$V" "$C" "$P" >> "$LOG" 2>&1 &
  local p=$!
  wait $p
  echo "=== $N $L exit rc=$? $(date -u +%FT%TZ)" >> "$LOG"
}

full_view() { echo "Slide $1 recreation — fidelity check vs original lecture frame"; }
full_cap()  { echo "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame"; }
crop_view() { echo "Slide $1 zoomed crop dense — render vs original at matched scale (rejudge 1)"; }
crop_cap()  { echo "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $1 (frame px $2) — $3"; }

D=$RJ
# 035 full + crop
leg 035 FULL "$D/slide035/judge_full.txt" 1200 "$D/slide035/render.png" "$NS/unique_slides/slide_035.jpg" "$(full_view 035)" "$(full_cap)" "$RJ/payload_A.txt" &
leg 035 CROP "$D/slide035/crop_dense_judge.txt" 600 "$D/slide035/crop_dense_render.png" "$D/slide035/crop_dense_orig.png" "$(crop_view 035)" "$(crop_cap 035 '376,160-680,368' 'Using Gradient Descent to train Linear Regression Model')" "$RJ/payload_B_035.txt" &
# 036 full + crop
leg 036 FULL "$D/slide036/judge_full.txt" 1200 "$D/slide036/render.png" "$NS/unique_slides/slide_036.jpg" "$(full_view 036)" "$(full_cap)" "$RJ/payload_A.txt" &
leg 036 CROP "$D/slide036/crop_dense_judge.txt" 600 "$D/slide036/crop_dense_render.png" "$D/slide036/crop_dense_orig.png" "$(crop_view 036)" "$(crop_cap 036 '64,112-368,320' 'Problem Formulation')" "$RJ/payload_B_036.txt" &
# 037 crop only (FULL=PASS banked in judge_full_retry.txt)
leg 037 CROP "$D/slide037/crop_dense_judge.txt" 600 "$D/slide037/crop_dense_render.png" "$D/slide037/crop_dense_orig.png" "$(crop_view 037)" "$(crop_cap 037 '60,136-344,344' 'Problem Formulation')" "$RJ/payload_B_037.txt" &
# 041 crop only (FULL FAIL dismissed 2026-10-30, judge_full_retry.txt)
leg 041 CROP "$D/slide041/crop_dense_judge.txt" 600 "$D/slide041/crop_dense_render.png" "$D/slide041/crop_dense_orig.png" "$(crop_view 041)" "$(crop_cap 041 '304,88-608,296' 'Check Classes of Points: Initial W and Step')" "$RJ/payload_B_041.txt" &
wait
echo "DRIVER_W01_DONE $(date -u +%FT%TZ)" >> "$LOG"
