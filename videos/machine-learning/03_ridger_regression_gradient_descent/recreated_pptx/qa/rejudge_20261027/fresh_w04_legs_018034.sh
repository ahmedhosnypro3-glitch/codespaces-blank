#!/usr/bin/env bash
# fresh_w04_legs_018034.sh — FRESH worker W04 2026-10-31: fill non-PASS result.txt legs
# in slides 018-034 (025 skipped) that have NO live vision_leg.sh wrapper on that leg.
# full leg -> judge_full_fresh.txt t=1200 payload_A.txt; crop leg -> crop_dense_judge_fresh.txt
# t=600 payload_B_0NN.txt. setsid-detached so legs survive this worker's exit.
# Evidence-only under qa/; never deletes transcripts; no git.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/fresh_w04_legs_018034.log
PIDS=$RJ/legs_20261031.pids

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
live_leg() { ps -eo args | grep '[v]ision_leg[.]sh' | grep -q "slide$1/$2"; }
title_of()  { sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=$((10#$1));" 2>/dev/null | head -1; }
region_of() { python3 "$RJ/pick_dense_region.py" "$1" 2>/dev/null | awk '{printf "%s,%s-%s,%s", $1,$2,$3,$4}'; }
legval() { grep -m1 "^$2=" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2- | awk '{print $1}'; }

launch_full() { # N
  local N=$1 D=$RJ/slide$N NN=$((10#$N)) OUT=$D/judge_full_fresh.txt T
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  setsid nohup bash "$RJ/vision_leg.sh" "$OUT" 1200 "$D/render.png" "$NS/unique_slides/slide_$N.jpg" \
    "Slide $NN recreation — fidelity check vs original lecture frame" \
    "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
    "$RJ/payload_A.txt" >> "$LOG" 2>&1 < /dev/null &
  echo "$! slide$N full judge_full_fresh.txt $(date -u +%FT%TZ)" >> "$PIDS"
  echo "LAUNCH $N F -> judge_full_fresh.txt pid=$! $(date -u +%FT%TZ)" >> "$LOG"
}
launch_crop() { # N
  local N=$1 D=$RJ/slide$N NN=$((10#$N)) OUT=$D/crop_dense_judge_fresh.txt T R
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  R=$(region_of "$N")
  setsid nohup bash "$RJ/vision_leg.sh" "$OUT" 600 "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
    "Slide $NN zoomed crop dense — render vs original at matched scale (rejudge 1)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $NN (frame px $R) — $T" \
    "$RJ/payload_B_$N.txt" >> "$LOG" 2>&1 < /dev/null &
  echo "$! slide$N crop crop_dense_judge_fresh.txt $(date -u +%FT%TZ)" >> "$PIDS"
  echo "LAUNCH $N C -> crop_dense_judge_fresh.txt pid=$! $(date -u +%FT%TZ)" >> "$LOG"
}

echo "fresh_w04_legs_018034 launch start $(date -u +%FT%TZ) pid=$$" >> "$LOG"
for N in 018 019 020 021 022 023 024 026 027 028 029 030 031 032 033 034; do
  D=$RJ/slide$N
  FV=$(legval "$N" FULL); CV=$(legval "$N" CROP)
  [ "$FV" = PASS ] || {
    if clean "$D/judge_full_fresh.txt"; then
      echo "SKIP $N F — clean fresh verdict already banked $(date -u +%FT%TZ)" >> "$LOG"
    elif live_leg "$N" judge_full; then
      echo "SKIP $N F — live wrapper on full leg $(date -u +%FT%TZ)" >> "$LOG"
    else
      launch_full "$N"; sleep 15
    fi
  }
  [ "$CV" = PASS ] || {
    if clean "$D/crop_dense_judge_fresh.txt"; then
      echo "SKIP $N C — clean fresh verdict already banked $(date -u +%FT%TZ)" >> "$LOG"
    elif live_leg "$N" crop_dense_judge; then
      echo "SKIP $N C — live wrapper on crop leg $(date -u +%FT%TZ)" >> "$LOG"
    else
      launch_crop "$N"; sleep 15
    fi
  }
done
echo "fresh_w04_legs_018034 launch end $(date -u +%FT%TZ)" >> "$LOG"
