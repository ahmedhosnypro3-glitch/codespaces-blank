#!/usr/bin/env bash
# fresh_fill_driver.sh — FRESH worker F01: fill missing rejudge legs for slides
# 035-051 of deck 03 (043/044/048 already done; 025 open = out of scope).
# Launches a leg ONLY if its transcript has no clean banked verdict AND no live
# vision_leg.sh process is working on that slide (never clobbers in-flight legs
# from other carriers). Self-healing: relaunches if a prior carrier died on
# 429 without a clean verdict. Read-only wrt deck bytes; evidence only under qa/.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/driver_F01.log
DONEF=$RJ/driver_F01.done
rm -f "$DONEF"
echo "F01 driver start $(date -u +%FT%TZ)" > "$LOG"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
live()  { pgrep -af 'vision_leg[.]sh' | grep -q "slide$1/"; }

title_of()  { sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=$((10#$1));" 2>/dev/null | head -1; }
region_of() { python3 "$RJ/pick_dense_region.py" "$1" 2>/dev/null | awk '{printf "%s,%s-%s,%s", $1,$2,$3,$4}'; }

launch_leg() { # N F|C
  local N=$1 L=$2 D=$RJ/slide$N NN=$((10#$N))
  local T R
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  R=$(region_of "$N")
  if [ "$L" = F ]; then
    nohup bash "$RJ/vision_leg.sh" "$D/judge_full.txt" 1200 "$D/render.png" "$NS/unique_slides/slide_$N.jpg" \
      "Slide $NN recreation — fidelity check vs original lecture frame" \
      "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
      "$RJ/payload_A.txt" >> "$LOG" 2>&1 &
  else
    nohup bash "$RJ/vision_leg.sh" "$D/crop_dense_judge.txt" 600 "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
      "Slide $NN zoomed crop dense — render vs original at matched scale (rejudge 1)" \
      "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $NN (frame px $R) — $T" \
      "$RJ/payload_B_$N.txt" >> "$LOG" 2>&1 &
  fi
  echo "LAUNCH $N $L pid=$! $(date -u +%FT%TZ)" >> "$LOG"
}

NEED="035:F 036:C 037:C 039:F 041:F 045:F 045:C 046:F 046:C 047:F 047:C 049:F 049:C 050:F 050:C 051:F 051:C"
deadline=$(( $(date +%s) + 21600 ))
while [ "$(date +%s)" -lt "$deadline" ]; do
  all=1
  for item in $NEED; do
    N=${item%%:*}; L=${item##*:}; D=$RJ/slide$N
    if [ "$L" = F ]; then OUT=$D/judge_full.txt; else OUT=$D/crop_dense_judge.txt; fi
    clean "$OUT" && continue
    all=0
    if live "$N"; then
      echo "WAIT  $N $L live-carrier $(date -u +%FT%TZ)" >> "$LOG"
    else
      launch_leg "$N" "$L"
      sleep 25
    fi
  done
  [ "$all" = 1 ] && break
  sleep 60
done
echo "F01 driver loop end $(date -u +%FT%TZ)" >> "$LOG"
for item in $NEED; do
  N=${item%%:*}; L=${item##*:}; D=$RJ/slide$N
  if [ "$L" = F ]; then OUT=$D/judge_full.txt; else OUT=$D/crop_dense_judge.txt; fi
  V=NORESULT
  if clean "$OUT"; then V=$(grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$OUT" | tail -1 | grep -oE 'PASS|FAIL'); fi
  echo "SUMMARY $N $L $V $(date -u +%FT%TZ)" >> "$LOG"
done
echo "F01_DONE $(date -u +%FT%TZ)" >> "$LOG"
touch "$DONEF"
