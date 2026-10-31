#!/usr/bin/env bash
# harvest_fresh2.sh — write result.txt for slides 001-017 from best clean verdicts.
# Priority: *_fresh2.txt (this worker's fresh legs) > *_fresh.txt > main > retry.
# A fresh2 verdict (PASS or FAIL) always supersedes; otherwise an existing PASS in
# result.txt is kept (never downgraded by stale banked FAILs); else best banked.
set -u
RJ=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
cd /home/codespace/ai_llm_slides
clean() {
  local f=$1
  [ -f "$f" ] || { echo NORESULT; return; }
  grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f" || { echo NORESULT; return; }
  grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)'
}
pick() { # D p1 p2... -> "VERDICT path" (first non-NORESULT)
  local d=$1; shift; local p v
  for p in "$@"; do v=$(clean "$d/$p"); [ "$v" != NORESULT ] && { echo "$v $d/$p"; return; }; done
  echo "NORESULT $d/$1"
}
for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
  D=$RJ/slide$N
  [ -f "$D/result.txt" ] || continue
  curF=$(grep -oE 'FULL=[A-Z]+' "$D/result.txt" | cut -d= -f2)
  curB=$(grep -oE 'CROP=[A-Z]+' "$D/result.txt" | cut -d= -f2)
  read -r FV FT <<< "$(pick "$D" judge_full_fresh2.txt judge_full_fresh.txt judge_full.txt judge_full_retry.txt)"
  read -r BV CT <<< "$(pick "$D" crop_dense_judge_fresh2.txt crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt)"
  f2F=$(clean "$D/judge_full_fresh2.txt"); f2B=$(clean "$D/crop_dense_judge_fresh2.txt")
  # fresh2 supersedes; else keep existing PASS; else banked pick
  if [ "$f2F" != NORESULT ]; then FV=$f2F; FT=$D/judge_full_fresh2.txt
  elif [ "$curF" = PASS ]; then FV=PASS; FT=$D/judge_full.txt
  fi
  if [ "$f2B" != NORESULT ]; then BV=$f2B; CT=$D/crop_dense_judge_fresh2.txt
  elif [ "$curB" = PASS ]; then BV=PASS; CT=$D/crop_dense_judge.txt
  fi
  TITLE=$(grep -m1 '^TITLE=' "$D/result.txt" | cut -d= -f2-)
  REGION=$(grep -m1 '^REGION=' "$D/result.txt" | cut -d= -f2-)
  NOTE=$(grep -m1 '^NOTE=' "$D/result.txt" | cut -d= -f2-)
  [ -n "$TITLE" ] || TITLE="slide $N"
  [ -n "$REGION" ] || REGION="?"
  {
    echo "SLIDE=$N"; echo "TITLE=$TITLE"
    echo "RENDER=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide$N/render.png"
    echo "REGION=$REGION"; echo "FULL=$FV"; echo "CROP=$BV"
    echo "FULL_TRANSCRIPT=$FT"; echo "CROP_TRANSCRIPT=$CT"
    [ -n "$NOTE" ] && echo "NOTE=$NOTE"
  } > "$D/result.txt.new" && mv "$D/result.txt.new" "$D/result.txt"
  echo "HARVEST $N FULL=$FV CROP=$BV"
done
