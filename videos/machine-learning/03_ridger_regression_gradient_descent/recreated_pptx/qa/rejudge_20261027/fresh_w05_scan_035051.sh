#!/usr/bin/env bash
# fresh_w05_scan_035051.sh — FRESH worker W05 (2026-10-31): scan slides 035-051 (skip 025)
# per dispatch: non-PASS result.txt legs with no live wrapper -> launch *_fresh.txt leg;
# PASS -> result.txt; FAIL -> PIL-first. Append-only evidence; never git/delete.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$RJ/legs_20261031.pids"
LOG=$RJ/fresh_w05_scan_035051.log
exec >> "$LOG" 2>&1
echo "W05 scan start $(date -u +%FT%TZ) pid=$$"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verd() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 | grep -oE 'PASS|FAIL'; }
resleg() { # N F|C -> first token of FULL=/CROP= in result.txt (or MISSING)
  local N=$1 L=$2 D=$RJ/slide$N
  [ -f "$D/result.txt" ] || { echo MISSING; return; }
  if [ "$L" = F ]; then grep -m1 '^FULL=' "$D/result.txt" | cut -d= -f2- | awk '{print $1}'
  else grep -m1 '^CROP=' "$D/result.txt" | cut -d= -f2- | awk '{print $1}'; fi
}
banked() { # N F|C -> newest clean transcript name + verdict, or NONE
  local N=$1 L=$2 D=$RJ/slide$N f best="" bv=""
  local pats
  if [ "$L" = F ]; then pats="judge_full_fresh4.txt judge_full_fresh3.txt judge_full_fresh2.txt judge_full_fresh.txt judge_full.txt judge_full_retry.txt"
  else pats="crop_dense_judge_fresh4.txt crop_dense_judge_fresh3.txt crop_dense_judge_fresh2.txt crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt"; fi
  for f in $pats; do
    if clean "$D/$f"; then best=$f; bv=$(verd "$D/$f"); break; fi
  done
  [ -n "$best" ] && echo "$best:$bv" || echo NONE
}
live() { # N F|C -> count of live vision_leg.sh carriers on that leg
  local N=$1 L=$2 pat
  if [ "$L" = F ]; then pat="slide$N/judge_full"; else pat="slide$N/crop_dense_judge"; fi
  pgrep -af 'vision_leg[.]sh' | grep -c "$pat"
}

for N in 035 036 037 038 039 040 041 042 043 044 045 046 047 048 049 050 051; do
  D=$RJ/slide$N
  for L in F C; do
    R=$(resleg "$N" "$L"); [ -z "$R" ] && R=EMPTY
    B=$(banked "$N" "$L")
    LV=$(live "$N" "$L")
    echo "SCAN $N $L result=$R banked=$B live=$LV"
  done
done
echo "occ_ps=$(ps -eo args | grep -c '[a]nalyze_image[.]py') legs=$(pgrep -c -f 'vision_leg[.]sh') $(date -u +%FT%TZ)"
echo "W05 scan end $(date -u +%FT%TZ)"
