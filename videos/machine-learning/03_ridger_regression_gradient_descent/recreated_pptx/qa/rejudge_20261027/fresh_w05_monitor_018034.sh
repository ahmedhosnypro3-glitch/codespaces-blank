#!/usr/bin/env bash
# fresh_w05_monitor_018034.sh — FRESH worker W05 2026-10-31: slides 018-034 (skip 25).
# Standing dispatch: for each result.txt leg that is not PASS:
#   - clean banked verdict landed (fresh -> plain -> retry) => harvest:
#       PASS -> surgical result.txt update; FAIL -> PIL-first via rejudge_adjudicate.py
#       (banked as slideN/adjudicate_w05_<leg>.txt) + register entry, result.txt keeps FAIL
#   - no live vision_leg.sh wrapper on that leg and no clean verdict => launch
#       setsid nohup vision_leg.sh <leg>_fresh.txt (full t=1200 payload_A, crop t=600 payload_B_0NN)
# Evidence-only under qa/; never deletes transcripts; never touches build/pptx/DB; no git.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$RJ/legs_20261031.pids"
LOG=$RJ/fresh_w05_monitor_018034.log
REG=$RJ/REJUDGE_REGISTER.md
SCOPE="018 019 020 021 022 023 024 026 027 028 029 030 031 032 033 034"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verdict() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 | grep -oE 'PASS|FAIL'; }
live_leg() { ps -eo args | grep '[v]ision_leg[.]sh' | grep -q "rejudge_20261027/slide$1/$2"; }
legval() { grep -m1 "^$2=" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2-; }
leg_is_pass() { case "$(legval "$1" "$2")" in PASS*) return 0;; *) return 1;; esac; }
STATE=$RJ/.w05_harvested
already_harvested() { # N kind file mtime
  grep -qF "$1 $2 $3 $4" "$STATE" 2>/dev/null
}
mark_harvested() { echo "$1 $2 $3 $4" >> "$STATE"; }
LSTATE=$RJ/.w05_launched
last_launch() { # N kind -> epoch of last launch, 0 if none
  awk -v n="$1" -v k="$2" '$1==n && $2==k {print $3}' "$LSTATE" 2>/dev/null | tail -1
}
mark_launch() { echo "$1 $2 $(date +%s)" >> "$LSTATE"; }
should_launch() { # N kind — true if no launch in the last 45 min
  local ll; ll=$(last_launch "$1" "$2"); ll=${ll:-0}
  [ $(( $(date +%s) - ll )) -gt 2700 ]
}
title_of() { sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=$((10#$1));" 2>/dev/null | head -1; }
region_of() { python3 "$RJ/pick_dense_region.py" "$1" 2>/dev/null | awk '{printf "%s,%s-%s,%s", $1,$2,$3,$4}'; }
ts_of() { stat -c %y "$1" | cut -d. -f1 | sed 's/ /_/'; }

# surgical result.txt update: only the named leg's value/transcript/ts lines change
set_leg() { # N FULL|CROP value transcript
  local N=$1 LEG=$2 VAL=$3 TR=$4 D=$RJ/slide$N F=$D/result.txt TMPF=$D/result.txt.w05tmp
  local vline tline tsline
  vline="$LEG=$VAL"; tline="${LEG}_TRANSCRIPT=$D/$TR"
  tsline="${LEG}_VERDICT_TS=$(ts_of "$D/$TR") UTC (clean, no 429)"
  awk -v vl="$vline" -v tl="$tline" -v sl="$tsline" -v leg="$LEG" '
    BEGIN { done_v=0; done_t=0; done_s=0 }
    $0 ~ "^"leg"=" { if (!done_v) { print vl; done_v=1 } next }
    $0 ~ "^"leg"_TRANSCRIPT=" { if (!done_t) { print tl; done_t=1 } next }
    $0 ~ "^"leg"_VERDICT_TS=" { if (!done_s) { print sl; done_s=1 } next }
    { print }
    END { if (!done_v) print vl; if (!done_t) print tl; if (!done_s) print sl }
  ' "$F" > "$TMPF" && mv "$TMPF" "$F"
}

launch_full() { # N
  local N=$1 D=$RJ/slide$N NN=$((10#$N)) OUT=$D/judge_full_fresh.txt T
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  setsid nohup bash "$RJ/vision_leg.sh" "$OUT" 1200 "$D/render.png" "$NS/unique_slides/slide_$N.jpg" \
    "Slide $NN recreation — fidelity check vs original lecture frame" \
    "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
    "$RJ/payload_A.txt" >> "$LOG" 2>&1 < /dev/null &
  echo "$! slide$N full judge_full_fresh.txt $(date -u +%FT%TZ)" >> "$RJ/legs_20261031.pids/w05.pids"
  echo "$(date -u +%FT%TZ) W05 LAUNCH $N FULL -> judge_full_fresh.txt pid=$!" >> "$LOG"
  mark_launch "$N" full
}
launch_crop() { # N
  local N=$1 D=$RJ/slide$N NN=$((10#$N)) OUT=$D/crop_dense_judge_fresh.txt T R
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  R=$(region_of "$N")
  [ -f "$RJ/payload_B_$N.txt" ] || { echo "$(date -u +%FT%TZ) W05 NO payload_B_$N.txt — skip crop launch $N" >> "$LOG"; return; }
  setsid nohup bash "$RJ/vision_leg.sh" "$OUT" 600 "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
    "Slide $NN zoomed crop dense — render vs original at matched scale (rejudge 1)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $NN (frame px $R) — $T" \
    "$RJ/payload_B_$N.txt" >> "$LOG" 2>&1 < /dev/null &
  echo "$! slide$N crop crop_dense_judge_fresh.txt $(date -u +%FT%TZ)" >> "$RJ/legs_20261031.pids/w05.pids"
  echo "$(date -u +%FT%TZ) W05 LAUNCH $N CROP -> crop_dense_judge_fresh.txt pid=$!" >> "$LOG"
  mark_launch "$N" crop
}

best_clean() { # N full|crop -> echoes "file verdict" of first clean among fresh/plain/retry
  local N=$1 D=$RJ/slide$N kind=$2 f
  if [ "$kind" = full ]; then flist="judge_full_fresh.txt judge_full.txt judge_full_retry.txt"
  else flist="crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt"; fi
  for f in $flist; do if clean "$D/$f"; then echo "$f $(verdict "$D/$f")"; return 0; fi; done
  return 1
}

reg() { echo "" >> "$REG"; echo "$1" >> "$REG"; }

harvest_leg() { # N full|crop
  local N=$1 kind=$2 D=$RJ/slide$N leg
  [ "$kind" = full ] && leg=FULL || leg=CROP
  leg_is_pass "$N" "$leg" && return 0
  local cur; cur=$(legval "$N" "$leg")
  local bc; bc=$(best_clean "$N" "$kind") || return 0
  local f=${bc%% *} v=${bc##* }
  local mt; mt=$(stat -c %Y "$D/$f")
  if already_harvested "$N" "$kind" "$f" "$mt"; then return 0; fi
  mark_harvested "$N" "$kind" "$f" "$mt"
  if [ "$v" = PASS ]; then
    set_leg "$N" "$leg" "PASS" "$f"
    echo "$(date -u +%FT%TZ) W05 HARVEST $N $leg=PASS from $f (was $cur)" >> "$LOG"
    reg "- $(date -u +%FT%TZ) W05 fresh worker: slide$N $leg clean PASS landed in \`$f\` -> result.txt $leg=PASS (was $cur)."
  else
    local mode=--full; [ "$kind" = crop ] && mode=--crop
    python3 "$RJ/rejudge_adjudicate.py" "$N" $mode > "$D/adjudicate_w05_${kind}.txt" 2>&1
    echo "$(date -u +%FT%TZ) W05 HARVEST $N $leg=FAIL from $f (was $cur); PIL census -> adjudicate_w05_${kind}.txt" >> "$LOG"
    reg "- $(date -u +%FT%TZ) W05 fresh worker: slide$N $leg clean FAIL landed in \`$f\` (was $cur). PIL-first adjudication census banked at \`slide$N/adjudicate_w05_${kind}.txt\`; result.txt left unchanged pending adjudication interpretation."
    # record FAIL in result.txt only when the leg had no verdict at all
    case "$cur" in NORESULT|NOVERDICT|pending|"") set_leg "$N" "$leg" "FAIL" "$f" ;;
    esac
    return 0
  fi
}

echo "$(date -u +%FT%TZ) W05 monitor start pid=$$ scope=018-034 skip 25" >> "$LOG"
ITER=0
while [ $ITER -lt 160 ]; do
  ITER=$((ITER+1))
  for N in $SCOPE; do
    D=$RJ/slide$N
    [ -f "$D/result.txt" ] || { echo "$(date -u +%FT%TZ) W05 $N: no result.txt, skip" >> "$LOG"; continue; }
    leg_is_pass "$N" FULL || {
      if bc=$(best_clean "$N" full); then harvest_leg "$N" full
      elif live_leg "$N" judge_full; then : # covered
      elif should_launch "$N" full; then launch_full "$N"; fi
    }
    leg_is_pass "$N" CROP || {
      if bc=$(best_clean "$N" crop); then harvest_leg "$N" crop
      elif live_leg "$N" crop_dense_judge; then : # covered
      elif should_launch "$N" crop; then launch_crop "$N"; fi
    }
  done
  sleep 150
done
echo "$(date -u +%FT%TZ) W05 monitor end" >> "$LOG"
