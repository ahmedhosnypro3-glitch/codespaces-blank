#!/usr/bin/env bash
# fresh_legs_018_034.sh — FRESH worker 2026-10-31: launch ONLY the missing rejudge
# legs for slides 018-034 of deck 03 (025 skipped: open under another worker's live
# leg). full leg: t=1200 payload_A.txt; crop leg: t=600 payload_B_0NN.txt.
# Skips any leg whose transcript is already clean (FINAL VERDICT, no 429) and never
# touches a slide with a live vision_leg.sh carrier. Evidence-only under qa/.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/fresh_legs_018034.log

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
live()  { ps -eo args | grep '[v]ision_leg[.]sh' | grep -q "slide$1/"; }
title_of()  { sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=$((10#$1));" 2>/dev/null | head -1; }
region_of() { python3 "$RJ/pick_dense_region.py" "$1" 2>/dev/null | awk '{printf "%s,%s-%s,%s", $1,$2,$3,$4}'; }

launch_full() { # N
  local N=$1 D=$RJ/slide$N NN=$((10#$N)) OUT=$D/judge_full.txt
  [ -f "$D/judge_full.txt" ] && OUT=$D/judge_full_fresh.txt
  nohup bash "$RJ/vision_leg.sh" "$OUT" 1200 "$D/render.png" "$NS/unique_slides/slide_$N.jpg" \
    "Slide $NN recreation — fidelity check vs original lecture frame" \
    "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
    "$RJ/payload_A.txt" >> "$LOG" 2>&1 &
  echo "LAUNCH $N F -> $(basename "$OUT") pid=$! $(date -u +%FT%TZ)" >> "$LOG"
}
launch_crop() { # N
  local N=$1 D=$RJ/slide$N NN=$((10#$N)) OUT=$D/crop_dense_judge.txt T R
  [ -f "$D/crop_dense_judge.txt" ] && OUT=$D/crop_dense_judge_fresh.txt
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  R=$(region_of "$N")
  nohup bash "$RJ/vision_leg.sh" "$OUT" 600 "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
    "Slide $NN zoomed crop dense — render vs original at matched scale (rejudge 1)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $NN (frame px $R) — $T" \
    "$RJ/payload_B_$N.txt" >> "$LOG" 2>&1 &
  echo "LAUNCH $N C -> $(basename "$OUT") pid=$! $(date -u +%FT%TZ)" >> "$LOG"
}

echo "fresh_legs_018_034 launch start $(date -u +%FT%TZ) pid=$$" >> "$LOG"
# slide:legs with MISSING legs only (banked-clean legs are skipped by the checks below)
NEED="030:both 031:crop 032:both 033:both 034:both"
for item in $NEED; do
  N=${item%%:*}; LEGS=$(echo "${item##*:}" | sed 's/\bboth\b/full crop/g'); D=$RJ/slide$N
  if live "$N"; then echo "SKIP $N — live carrier on slide" >> "$LOG"; continue; fi
  for leg in $LEGS; do
    case $leg in
      full)
        if clean "$D/judge_full.txt" || clean "$D/judge_full_retry.txt" || clean "$D/judge_full_fresh.txt"; then
          echo "SKIP $N F — clean verdict already banked $(date -u +%FT%TZ)" >> "$LOG"
        else
          launch_full "$N"; sleep 20
        fi ;;
      crop)
        if clean "$D/crop_dense_judge.txt" || clean "$D/crop_dense_judge_retry.txt" || clean "$D/crop_dense_judge_fresh.txt"; then
          echo "SKIP $N C — clean verdict already banked $(date -u +%FT%TZ)" >> "$LOG"
        else
          launch_crop "$N"; sleep 20
        fi ;;
    esac
  done
done
echo "fresh_legs_018_034 launch end $(date -u +%FT%TZ)" >> "$LOG"
