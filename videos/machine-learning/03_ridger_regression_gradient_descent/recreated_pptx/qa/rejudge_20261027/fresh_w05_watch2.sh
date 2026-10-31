#!/usr/bin/env bash
# fresh_w05_watch2.sh — W05 bounded watch over the only non-PASS slides in
# 035-051: 045, 050, 051 (025 skipped per dispatch). Never calls write_result.sh
# (it cannot see *_fresh2/3 transcripts and clobbered slide046 once) — it only
# logs banked verdicts, PIL-first-adjudicates FAILs, and launches a fresh leg
# when a leg has no clean banked verdict AND no live carrier.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$RJ/legs_20261031.pids"
cd "$ROOT"
LOG=$RJ/fresh_w05_watch2.log
exec >> "$LOG" 2>&1

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verd() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 | grep -oE 'PASS|FAIL'; }
resleg() {
  local N=$1 L=$2 D=$RJ/slide$N
  [ -f "$D/result.txt" ] || { echo MISSING; return; }
  if [ "$L" = F ]; then grep -m1 '^FULL=' "$D/result.txt" | cut -d= -f2- | awk '{print $1}'
  else grep -m1 '^CROP=' "$D/result.txt" | cut -d= -f2- | awk '{print $1}'; fi
}
banked() {
  local N=$1 L=$2 D=$RJ/slide$N f best="" bv="" pats
  if [ "$L" = F ]; then pats="judge_full_fresh4.txt judge_full_fresh3.txt judge_full_fresh2.txt judge_full_fresh.txt judge_full.txt judge_full_retry.txt"
  else pats="crop_dense_judge_fresh4.txt crop_dense_judge_fresh3.txt crop_dense_judge_fresh2.txt crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt"; fi
  for f in $pats; do if clean "$D/$f"; then best=$f; bv=$(verd "$D/$f"); break; fi; done
  [ -n "$best" ] && echo "$best:$bv" || echo NONE
}
live() {
  local N=$1 L=$2 pat
  if [ "$L" = F ]; then pat="slide$N/judge_full"; else pat="slide$N/crop_dense_judge"; fi
  pgrep -af 'vision_leg[.]sh' | grep -c "$pat"
}
nextfree() {
  local N=$1 L=$2 D=$RJ/slide$N f
  if [ "$L" = F ]; then for f in judge_full_fresh5.txt judge_full_fresh4.txt judge_full_fresh6.txt; do
    [ -e "$D/$f" ] || { echo "$f"; return; }
  done; else for f in crop_dense_judge_fresh5.txt crop_dense_judge_fresh4.txt crop_dense_judge_fresh6.txt; do
    [ -e "$D/$f" ] || { echo "$f"; return; }
  done; fi; echo ""
}
launch() {
  local N=$1 L=$2 T=$3 D=$RJ/slide$N NN=$((10#$N)) TMO IMG1 IMG2 VIEW CAP PAY
  if [ "$L" = F ]; then
    TMO=1200; IMG1=$D/render.png; IMG2=$NS/unique_slides/slide_$N.jpg; PAY=$RJ/payload_A.txt
    VIEW="Slide $NN recreation — fidelity check vs original lecture frame"
    CAP="IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame"
  else
    TMO=600; IMG1=$D/crop_dense_render.png; IMG2=$D/crop_dense_orig.png; PAY=$RJ/payload_B_$N.txt
    VIEW="Slide $NN zoomed crop — fidelity check vs original"
    CAP="IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame"
  fi
  [ -f "$PAY" ] || { echo "MISSING payload $PAY"; return 2; }
  setsid nohup bash "$RJ/vision_leg.sh" "$D/$T" "$TMO" "$IMG1" "$IMG2" "$VIEW" "$CAP" "$PAY" > "$D/$T.wrapper.out" 2>&1 &
  echo $! > "$RJ/legs_20261031.pids/${N}_${L}_w05.pid"
  echo "LAUNCH $N $L -> $T pid $! $(date -u +%FT%TZ)"
}

echo "W05 watch2 start $(date -u +%FT%TZ) pid=$$ deadline=$(( $(date +%s) + 2400 ))"
while [ "$(date +%s)" -lt $(( $(date +%s) + 2400 )) ]; do
  echo "=== pass $(date -u +%FT%TZ) ==="
  for N in 045 050 051; do
    D=$RJ/slide$N
    for L in F C; do
      R=$(resleg "$N" "$L"); [ -z "$R" ] && R=EMPTY
      B=$(banked "$N" "$L"); LV=$(live "$N" "$L")
      case "$R" in PASS) echo "$N $L result=PASS banked=$B live=$LV"; continue;; esac
      if [ "$B" != NONE ]; then
        BV=${B##*:}
        echo "$N $L result=$R BANKED $B live=$LV"
        if [ "$BV" = FAIL ]; then
          if [ "$L" = F ]; then AJ=$D/adjudicate_w05_full.txt; MODE=--full; else AJ=$D/adjudicate_w05_crop.txt; MODE=--crop; fi
          if [ ! -f "$AJ" ]; then
            python3 "$RJ/rejudge_adjudicate.py" "$N" "$MODE" > "$AJ" 2>&1 && echo "$N $L FAIL PIL-first banked $AJ" || echo "$N $L PIL-first rc=$?"
          fi
        fi
      else
        if [ "$LV" -gt 0 ]; then
          echo "$N $L result=$R no-banked live=$LV waiting"
        else
          T=$(nextfree "$N" "$L")
          if [ -n "$T" ]; then launch "$N" "$L" "$T" || echo "$N $L launch aborted"; else echo "$N $L no free name"; fi
        fi
      fi
    done
  done
  sleep 45
done
echo "W05 watch2 end $(date -u +%FT%TZ)"
