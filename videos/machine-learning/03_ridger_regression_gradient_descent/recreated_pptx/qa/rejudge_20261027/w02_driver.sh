#!/usr/bin/env bash
# w02_driver.sh — fresh worker W01 (second batch): fill ALL missing rejudge legs for
# certified slides 045,046,047,049,050,051 (FULL t=1200 payload_A + CROP t=600 payload_B_0NN).
# Prior chain 561419 was stopped by this worker to avoid dual writers on the same
# transcript paths; its banked transcripts (e.g. slide042) remain on disk untouched.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/driver_W02.log

leg() { # N L OUT TMO I1 I2 V C P
  local N=$1 L=$2 OUT=$3 TMO=$4 I1=$5 I2=$6 V=$7 C=$8 P=$9
  echo "=== $N $L start $(date -u +%FT%TZ)" >> "$LOG"
  nohup bash "$RJ/vision_leg.sh" "$OUT" "$TMO" "$I1" "$I2" "$V" "$C" "$P" >> "$LOG" 2>&1 &
  wait $!
  echo "=== $N $L exit rc=$? $(date -u +%FT%TZ)" >> "$LOG"
}

declare -A TITLE REGION
TITLE[045]="Iteration 4";                                          REGION[045]="60,88-344,296"
TITLE[046]="Perceptron Algorithm: Iteration 4 — Stop Iterations";  REGION[046]="60,88-344,296"
TITLE[047]="Check Classes of Z Vectors";                           REGION[047]="60,88-344,296"
TITLE[049]="Iteration 2";                                          REGION[049]="60,88-344,296"
TITLE[050]="Iteration 2";                                          REGION[050]="60,88-344,296"
TITLE[051]="Check Classes";                                        REGION[051]="60,88-344,296"

for N in 045 046 047 049 050 051; do
  D=$RJ/slide$N
  NN=$((10#$N))
  # full leg only if no clean verdict banked
  if [ ! -f "$D/judge_full.txt" ] || ! grep -q 'FINAL VERDICT' "$D/judge_full.txt" 2>/dev/null || grep -qi '429' "$D/judge_full.txt" 2>/dev/null; then
    leg $N FULL "$D/judge_full.txt" 1200 "$D/render.png" "$NS/unique_slides/slide_${N}.jpg" \
      "Slide $NN recreation — fidelity check vs original lecture frame" \
      "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
      "$RJ/payload_A.txt" &
  else echo "=== $N FULL already banked" >> "$LOG"; fi
  # crop leg only if no clean verdict banked
  if [ ! -f "$D/crop_dense_judge.txt" ] || ! grep -q 'FINAL VERDICT' "$D/crop_dense_judge.txt" 2>/dev/null || grep -qi '429' "$D/crop_dense_judge.txt" 2>/dev/null; then
    leg $N CROP "$D/crop_dense_judge.txt" 600 "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
      "Slide $NN zoomed crop dense — render vs original at matched scale (rejudge 1)" \
      "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $NN (frame px ${REGION[$N]}) — ${TITLE[$N]}" \
      "$RJ/payload_B_${N}.txt" &
  else echo "=== $N CROP already banked" >> "$LOG"; fi
done
wait
echo "DRIVER_W02_DONE $(date -u +%FT%TZ)" >> "$LOG"
