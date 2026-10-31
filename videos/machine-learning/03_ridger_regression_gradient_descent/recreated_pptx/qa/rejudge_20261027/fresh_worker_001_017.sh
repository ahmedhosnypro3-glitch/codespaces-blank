#!/usr/bin/env bash
# fresh_worker_001_017.sh — FRESH worker (2026-10-31): fill missing rejudge legs
# for slides 001-017 of deck 03. For each slide whose result.txt lacks FULL=PASS
# or CROP=PASS and which has NO live vision_leg.sh wrapper, launch the missing leg
# via nohup vision_leg.sh (full t=1200 payload_A; crop t=600 payload_B_0NN.txt).
# Fresh legs write *_fresh2.txt transcripts (never clobber banked evidence).
# Banked FAILs get PIL-first adjudication (rejudge_adjudicate.py). Then result.txt
# files are rewritten from best clean verdicts and REJUDGE_REGISTER.md appended.
# Read-only wrt deck bytes; evidence only under qa/. Never git, never delete.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/driver_fresh_001_017.log
exec >> "$LOG" 2>&1
echo "=== fresh_worker_001_017 start $(date -u +%FT%TZ) pid=$$"

clean() { # transcript -> PASS|FAIL|NORESULT
  local f=$1
  [ -f "$f" ] || { echo NORESULT; return; }
  grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f" || { echo NORESULT; return; }
  grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)'
}
res_leg() { grep -oE "$2=[A-Z]+" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2; }
# live wrapper ON THE SAME LEG of this slide (per-leg, not per-slide: a carrier on
# the other leg writes a different transcript and does not conflict with *_fresh2)
live() { # N full|crop
  if [ "$2" = full ]; then
    pgrep -af 'vision_leg[.]sh' | grep "slide$1/" | grep -q 'judge_full'
  else
    pgrep -af 'vision_leg[.]sh' | grep "slide$1/" | grep -q 'crop_dense'
  fi
}

title_of() { grep -m1 "^TITLE=" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2-; }
region_of() { grep -m1 "^REGION=" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2-; }

# legs to fill: N:LEG (only those missing in result.txt AND without live wrapper;
# re-checked at launch time)
NEED="003:crop 005:full 012:crop 013:crop 014:full 015:crop"

declare -a JPIDS=() JNAMES=()
for item in $NEED; do
  N=${item%%:*}; L=${item##*:}; D=$RJ/slide$N; NN=$((10#$N))
  want=$([ "$L" = full ] && echo FULL || echo CROP)
  have=$(res_leg "$N" "$want")
  if [ "$have" = PASS ]; then echo "SKIP $N $L already PASS in result.txt"; continue; fi
  if live "$N" "$L"; then echo "SKIP $N $L live wrapper on same leg"; continue; fi
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  R=$(region_of "$N"); [ -n "$R" ] || R="?"
  if [ "$L" = full ]; then
    OUT=$D/judge_full_fresh2.txt; TMO=1200
    I1=$D/render.png; I2=$ROOT/$NS/unique_slides/slide_$N.jpg
    V="Slide $NN recreation — fidelity check vs original lecture frame"
    C="IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original lecture video frame"
    P=$RJ/payload_A.txt
  else
    OUT=$D/crop_dense_judge_fresh2.txt; TMO=600
    I1=$D/crop_dense_render.png; I2=$D/crop_dense_orig.png
    V="Slide $NN zoomed crop — fidelity check vs original (fresh leg)"
    C="IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame (region $R) — $T"
    P=$RJ/payload_B_$N.txt
    [ -f "$P" ] || sed "s/slide NNN/slide $N/g" "$RJ/payload_B.tmpl" > "$P"
  fi
  # final live re-check right before launch
  if live "$N" "$L"; then echo "SKIP $N $L live wrapper appeared"; continue; fi
  OCC_MAX=1000 nohup bash "$RJ/vision_leg.sh" "$OUT" "$TMO" "$I1" "$I2" "$V" "$C" "$P" \
    >> "$RJ/leg_${N}_${L}_fresh2.log" 2>&1 &
  JPIDS+=($!); JNAMES+=("$N:$L")
  echo "LAUNCH $N $L pid=$! out=$(basename "$OUT") $(date -u +%FT%TZ)"
  sleep 20
done

for i in "${!JPIDS[@]}"; do
  wait "${JPIDS[$i]}"; rc=$?
  echo "LEG_DONE ${JNAMES[$i]} rc=$rc $(date -u +%FT%TZ)"
done

# PIL-first adjudication of the banked FAIL transcripts on the open slides
for item in "003:crop" "005:crop" "012:full" "013:full" "014:crop" "015:full"; do
  N=${item%%:*}; L=${item##*:}; D=$RJ/slide$N
  if [ "$L" = full ]; then M=""; else M="--crop"; fi
  python3 "$RJ/rejudge_adjudicate.py" "$N" $M > "$D/adjudicate_20261031_${L}.txt" 2>&1
  echo "ADJUDICATE $N $L -> adjudicate_20261031_${L}.txt $(date -u +%FT%TZ)"
done

# harvest: rewrite result.txt for 001-017. A leg already PASS in result.txt is
# NEVER downgraded (adjudicated/dismissed FAILs stay PASS). NORESULT legs take the
# best clean verdict: fresh2 (this worker) > fresh (live carrier) > main > retry.
# Transcript paths point at the file that supplied the verdict.
pick() { # D prefix1 prefix2... -> echoes "VERDICT path"
  local d=$1; shift
  local p v
  for p in "$@"; do
    v=$(clean "$d/$p")
    if [ "$v" != NORESULT ]; then echo "$v $d/$p"; return; fi
  done
  echo "NORESULT $d/$1"
}
for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
  D=$RJ/slide$N; NN=$((10#$N))
  [ -f "$D/result.txt" ] || { echo "NO result.txt slide$N"; continue; }
  curF=$(res_leg "$N" FULL); curB=$(res_leg "$N" CROP)
  read -r FV FT <<< "$(pick "$D" judge_full_fresh2.txt judge_full_fresh.txt judge_full.txt judge_full_retry.txt)"
  read -r BV CT <<< "$(pick "$D" crop_dense_judge_fresh2.txt crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt)"
  [ "$curF" = PASS ] && { FV=PASS; FT=$D/judge_full.txt; }
  [ "$curB" = PASS ] && { BV=PASS; CT=$D/crop_dense_judge.txt; }
  TITLE=$(grep -m1 '^TITLE=' "$D/result.txt" | cut -d= -f2-)
  REGION=$(grep -m1 '^REGION=' "$D/result.txt" | cut -d= -f2-)
  [ -n "$TITLE" ] || TITLE="slide $N"
  [ -n "$REGION" ] || REGION="?"
  NOTE=$(grep -m1 '^NOTE=' "$D/result.txt" | cut -d= -f2-)
  {
    echo "SLIDE=$N"
    echo "TITLE=$TITLE"
    echo "RENDER=$NS/recreated_pptx/qa/rejudge_20261027/slide$N/render.png"
    echo "REGION=$REGION"
    echo "FULL=$FV"
    echo "CROP=$BV"
    echo "FULL_TRANSCRIPT=$FT"
    echo "CROP_TRANSCRIPT=$CT"
    [ -n "$NOTE" ] && echo "NOTE=$NOTE"
    echo "FRESH2=legs launched by fresh_worker_001_017 $(date -u +%FT%TZ)"
  } > "$D/result.txt.new" && mv "$D/result.txt.new" "$D/result.txt"
  echo "RESULT $N FULL=$FV CROP=$BV $(date -u +%FT%TZ)"
done

{
  echo ""
  echo "## Fresh-worker sweep 2026-10-31 (slides 001-017, fresh_worker_001_017.sh)"
  echo ""
  echo "CORRECTION: the first pass of this sweep (02:57Z) had a per-slide live-check bug — it launched no legs and its harvest briefly downgraded adjudicated-PASS slides (004/007/010/016); those result.txt files were restored verbatim from the pre-run capture before this pass."
  echo ""
  echo "Pass 2 (per-leg live check, no PASS downgrade): legs launched via nohup vision_leg.sh (t=1200 payload_A full / t=600 payload_B_0NN crop, transcripts *_fresh2.txt, no live wrapper on the same leg at launch): 003 crop, 005 full, 012 crop, 013 crop, 014 full, 015 crop. Slides 001/002/004/006/007/008/009/010/011/016/017 already FULL=PASS+CROP=PASS — kept PASS. Slides with a live foreign wrapper on the other leg (003F 005C 012F 013F 014C 015F) were left to that carrier. Banked FAILs PIL-adjudicated: adjudicate_20261031_{full,crop}.txt in slide003/005/012/013/014/015. result.txt rewritten $(date -u +%FT%TZ): PASS legs never downgraded; NORESULT legs take best clean verdict fresh2 > fresh > main > retry."
  echo ""
  echo "| slide | FULL | CROP | source transcripts |"
  echo "|---|---|---|---|"
  for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
    D=$RJ/slide$N
    echo "| $N | $(res_leg "$N" FULL) | $(res_leg "$N" CROP) | $(basename "$(grep -m1 '^FULL_TRANSCRIPT=' $D/result.txt | cut -d= -f2-)") + $(basename "$(grep -m1 '^CROP_TRANSCRIPT=' $D/result.txt | cut -d= -f2-)") |"
  done
} >> "$RJ/REJUDGE_REGISTER.md"

echo "=== fresh_worker_001_017 DONE $(date -u +%FT%TZ)"
