#!/usr/bin/env bash
# fresh_worker_001_017b.sh — FRESH worker (2026-10-31, spawn B): fill missing rejudge
# legs for slides 001-017 of deck 03. For each slide0N whose result.txt lacks
# FULL=PASS or CROP=PASS AND whose missing leg has NO live vision_leg.sh wrapper,
# launch the leg via nohup vision_leg.sh (full t=1200 payload_A / crop t=600
# payload_B_0NN.txt). Fresh legs write *_fresh3.txt transcripts (never clobber
# banked evidence). FAIL legs get PIL-first adjudication (rejudge_adjudicate.py)
# when adjudicate_20261031_<leg>.txt is absent. Then result.txt is rewritten from
# best clean verdicts and REJUDGE_REGISTER.md appended.
# Read-only wrt deck bytes; evidence only under qa/. Never git, never delete.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/driver_fresh_001_017b.log
exec >> "$LOG" 2>&1
echo "=== fresh_worker_001_017b start $(date -u +%FT%TZ) pid=$$"

clean() { # transcript -> PASS|FAIL|NORESULT
  local f=$1
  [ -f "$f" ] || { echo NORESULT; return; }
  grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f" || { echo NORESULT; return; }
  grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)'
}
res_leg() { grep -oE "$2=[A-Z]+" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2; }
leg_live() { # N full|crop — live wrapper on that leg of that slide
  local n=$1 l=$2 pat
  [ "$l" = full ] && pat='judge_full' || pat='crop'
  pgrep -af 'vision_leg[.]sh' | grep "slide$n/" | grep -q "$pat"
}

title_of() { grep -m1 "^TITLE=" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2-; }
region_of() { grep -m1 "^REGION=" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2-; }

declare -a JPIDS=() JNAMES=()
for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
  D=$RJ/slide$N; NN=$((10#$N))
  for L in full crop; do
    want=$([ "$L" = full ] && echo FULL || echo CROP)
    have=$(res_leg "$N" "$want")
    if [ "$have" = PASS ]; then continue; fi
    if leg_live "$N" "$L"; then echo "SKIP $N $L live wrapper present"; continue; fi
    T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
    R=$(region_of "$N"); [ -n "$R" ] || R="?"
    if [ "$L" = full ]; then
      OUT=$D/judge_full_fresh3.txt; TMO=1200
      I1=$D/render.png; I2=$ROOT/$NS/unique_slides/slide_$N.jpg
      V="Slide $NN recreation — fidelity check vs original lecture frame (fresh leg B)"
      C="IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original lecture video frame"
      P=$RJ/payload_A.txt
    else
      OUT=$D/crop_dense_judge_fresh3.txt; TMO=600
      I1=$D/crop_dense_render.png; I2=$D/crop_dense_orig.png
      V="Slide $NN zoomed crop — fidelity check vs original (fresh leg B)"
      C="IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame (region $R) — $T"
      P=$RJ/payload_B_$N.txt
      [ -f "$P" ] || sed "s/slide NNN/slide $N/g" "$RJ/payload_B.tmpl" > "$P"
    fi
    if leg_live "$N" "$L"; then echo "SKIP $N $L live wrapper appeared"; continue; fi
    OCC_MAX=1000 setsid nohup bash "$RJ/vision_leg.sh" "$OUT" "$TMO" "$I1" "$I2" "$V" "$C" "$P" \
      >> "$RJ/leg_${N}_${L}_fresh3.log" 2>&1 < /dev/null &
    JPIDS+=($!); JNAMES+=("$N:$L")
    echo "LAUNCH $N $L pid=$! out=$(basename "$OUT") $(date -u +%FT%TZ)"
    sleep 20
  done
done

for i in "${!JPIDS[@]}"; do
  wait "${JPIDS[$i]}"; rc=$?
  echo "LEG_DONE ${JNAMES[$i]} rc=$rc $(date -u +%FT%TZ)"
done
[ ${#JPIDS[@]} -eq 0 ] && echo "NO_LEGS_LAUNCHED $(date -u +%FT%TZ)"

# PIL-first adjudication for any FAIL leg in 001-017 lacking adjudicate_20261031_<leg>.txt
for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
  D=$RJ/slide$N
  for L in full crop; do
    [ "$L" = full ] && M="" || M="--crop"
    # any clean FAIL among candidate transcripts?
    fail=0
    for t in judge_full_fresh3.txt judge_full_fresh2.txt judge_full_fresh.txt judge_full.txt judge_full_retry.txt; do
      [ "$L" = crop ] && continue
      [ "$(clean "$D/$t")" = FAIL ] && fail=1
    done
    for t in crop_dense_judge_fresh3.txt crop_dense_judge_fresh2.txt crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt; do
      [ "$L" = full ] && continue
      [ "$(clean "$D/$t")" = FAIL ] && fail=1
    done
    [ $fail -eq 1 ] || continue
    A=$D/adjudicate_20261031_${L}.txt
    if [ ! -f "$A" ]; then
      python3 "$RJ/rejudge_adjudicate.py" "$N" $M > "$A" 2>&1
      echo "ADJUDICATE $N $L -> $A $(date -u +%FT%TZ)"
    else
      echo "ADJUDICATE $N $L already banked ($A)"
    fi
  done
done

# harvest: rewrite result.txt for 001-017 from best clean verdicts
for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
  D=$RJ/slide$N; NN=$((10#$N))
  [ -f "$D/result.txt" ] || { echo "NO result.txt slide$N"; continue; }
  FV=NORESULT; FT=""
  for t in judge_full_fresh3.txt judge_full_fresh2.txt judge_full_fresh.txt judge_full.txt judge_full_retry.txt; do
    v=$(clean "$D/$t"); if [ "$v" != NORESULT ] && [ -z "$FT" ]; then FV=$v; FT=$D/$t; fi
  done
  BV=NORESULT; CT=""
  for t in crop_dense_judge_fresh3.txt crop_dense_judge_fresh2.txt crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt; do
    v=$(clean "$D/$t"); if [ "$v" != NORESULT ] && [ -z "$CT" ]; then BV=$v; CT=$D/$t; fi
  done
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
    echo "FRESH3=legs launched by fresh_worker_001_017b $(date -u +%FT%TZ)"
  } > "$D/result.txt.new" && mv "$D/result.txt.new" "$D/result.txt"
  echo "RESULT $N FULL=$FV CROP=$BV $(date -u +%FT%TZ)"
done

{
  echo ""
  echo "## Fresh-worker spawn B 2026-10-31 (slides 001-017, fresh_worker_001_017b.sh)"
  echo ""
  echo "Missing legs (not PASS, no live wrapper at launch) filled via nohup vision_leg.sh — transcripts *_fresh3.txt, logs leg_N_L_fresh3.log; full t=1200 payload_A, crop t=600 payload_B_0NN.txt. Legs with a live foreign wrapper were left to that carrier. FAIL legs PIL-adjudicated via rejudge_adjudicate.py (adjudicate_20261031_<leg>.txt where absent). result.txt rewritten from best clean verdicts $(date -u +%FT%TZ). No git; no evidence deleted."
  echo ""
  echo "| slide | FULL | CROP | source transcripts |"
  echo "|---|---|---|---|"
  for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
    D=$RJ/slide$N
    echo "| $N | $(res_leg "$N" FULL) | $(res_leg "$N" CROP) | $(basename "$(grep -m1 '^FULL_TRANSCRIPT=' $D/result.txt | cut -d= -f2-)") + $(basename "$(grep -m1 '^CROP_TRANSCRIPT=' $D/result.txt | cut -d= -f2-)") |"
  done
} >> "$RJ/REJUDGE_REGISTER.md"

echo "=== fresh_worker_001_017b DONE $(date -u +%FT%TZ)"
