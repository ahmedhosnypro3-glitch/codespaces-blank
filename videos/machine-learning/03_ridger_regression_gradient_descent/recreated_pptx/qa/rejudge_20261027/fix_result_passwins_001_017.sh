#!/usr/bin/env bash
# fix_result_passwins_001_017.sh — repair result.txt for slides 001-017 after
# fresh_worker_001_017b's first-found harvest degraded PASS legs (stale FAIL
# transcripts picked ahead of banked PASS; live-wrapper rm -f made one leg look
# NORESULT). Recompute with PASS-wins precedence over ALL candidate transcripts.
# Never deletes; only rewrites result.txt via .new+mv. No git.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/driver_fix_passwins.log
exec >> "$LOG" 2>&1
echo "=== fix_passwins start $(date -u +%FT%TZ) pid=$$"

clean() {
  local f=$1
  [ -f "$f" ] || { echo NORESULT; return; }
  grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f" || { echo NORESULT; return; }
  grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)'
}

harvest() { # dir prefix-glob -> VERDICT TRANSCRIPT (PASS wins over FAIL wins over NORESULT)
  local d=$1 pat=$2 v best="" bt=""
  local pass_t="" fail_t=""
  for f in $d/$pat; do
    [ -f "$f" ] || continue
    v=$(clean "$f")
    [ "$v" = PASS ] && { [ -z "$pass_t" ] && pass_t=$f; }
    [ "$v" = FAIL ] && { [ -z "$fail_t" ] && fail_t=$f; }
  done
  if [ -n "$pass_t" ]; then echo "PASS $pass_t"; return; fi
  if [ -n "$fail_t" ]; then echo "FAIL $fail_t"; return; fi
  echo "NORESULT "
}

for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
  D=$RJ/slide$N
  [ -f "$D/result.txt" ] || { echo "NO result.txt slide$N"; continue; }
  read -r FV FT <<< "$(harvest "$D" 'judge_full*.txt')"
  read -r BV CT <<< "$(harvest "$D" 'crop_dense_judge*.txt')"
  TITLE=$(grep -m1 '^TITLE=' "$D/result.txt" | cut -d= -f2-)
  REGION=$(grep -m1 '^REGION=' "$D/result.txt" | cut -d= -f2-)
  NOTE=$(grep -m1 '^NOTE=' "$D/result.txt" | cut -d= -f2-)
  [ -n "$TITLE" ] || TITLE="slide $N"
  [ -n "$REGION" ] || REGION="?"
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
    echo "PASSWINS=result recomputed PASS-wins by fix_result_passwins_001_017.sh $(date -u +%FT%TZ)"
  } > "$D/result.txt.new" && mv "$D/result.txt.new" "$D/result.txt"
  echo "FIXED $N FULL=$FV CROP=$BV $(date -u +%FT%TZ)"
done
echo "=== fix_passwins DONE $(date -u +%FT%TZ)"
