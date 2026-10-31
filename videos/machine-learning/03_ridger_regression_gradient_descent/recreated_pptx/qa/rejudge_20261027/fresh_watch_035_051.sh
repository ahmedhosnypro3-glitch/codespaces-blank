#!/usr/bin/env bash
# fresh_watch_035_051.sh — FRESH worker W03 watchdog for deck-03 rejudge slides
# 045 046 047 049 050 051 (025 skipped per dispatch; 043/044/048 already done).
# Launches a leg via launch_leg.sh ONLY when its transcript has no clean banked
# verdict (FINAL VERDICT + no 429) AND no live vision_leg.sh carrier is working
# that exact leg (never clobbers in-flight work). Self-heals 429 deaths.
# Evidence-only under qa/rejudge_20261027/. Never git, never delete.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/driver_W03.log
echo "W03 watchdog start $(date -u +%FT%TZ) pid=$$" >> "$LOG"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
leg_clean() { # N F|C
  local N=$1 L=$2 D=$RJ/slide$N f
  if [ "$L" = F ]; then
    for f in judge_full_fresh.txt judge_full.txt judge_full_retry.txt; do clean "$D/$f" && return 0; done
  else
    for f in crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt; do clean "$D/$f" && return 0; done
  fi
  return 1
}
live_leg() { # N F|C — carrier whose argv contains slideN/<transcript>
  local N=$1 L=$2 pat
  if [ "$L" = F ]; then pat="slide$N/judge_full"; else pat="slide$N/crop_dense_judge"; fi
  pgrep -af 'vision_leg[.]sh' | grep -q "$pat"
}
SLIDES="045 046 047 049 050 051"
deadline=$(( $(date +%s) + 21600 ))
while [ "$(date +%s)" -lt "$deadline" ]; do
  all=1
  for N in $SLIDES; do
    for L in F C; do
      if leg_clean "$N" "$L"; then continue; fi
      all=0
      if live_leg "$N" "$L"; then
        echo "WAIT  $N $L live-carrier $(date -u +%FT%TZ)" >> "$LOG"
      else
        if [ "$L" = F ]; then LEG=full; else LEG=crop; fi
        bash "$RJ/launch_leg.sh" "$N" "$LEG"
        echo "LAUNCH $N $L via launch_leg.sh $(date -u +%FT%TZ)" >> "$LOG"
        sleep 20
      fi
    done
  done
  [ "$all" = 1 ] && break
  sleep 45
done
echo "W03 watchdog loop end $(date -u +%FT%TZ)" >> "$LOG"
for N in $SLIDES; do
  for L in F C; do
    V=NORESULT; D=$RJ/slide$N
    if [ "$L" = F ]; then fs="judge_full_fresh.txt judge_full.txt judge_full_retry.txt"; else fs="crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt"; fi
    for f in $fs; do
      if clean "$D/$f"; then V="$(grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$D/$f" | tail -1 | grep -oE 'PASS|FAIL') $f"; break; fi
    done
    echo "SUMMARY $N $L $V $(date -u +%FT%TZ)" >> "$LOG"
  done
done
echo "W03_DONE $(date -u +%FT%TZ)" >> "$LOG"
