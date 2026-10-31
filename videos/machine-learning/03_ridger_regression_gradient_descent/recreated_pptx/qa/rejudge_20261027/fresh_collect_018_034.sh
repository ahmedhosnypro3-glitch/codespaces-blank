#!/usr/bin/env bash
# fresh_collect_018_034.sh — resolve clean banked verdicts for slides 018-034
# (025 skipped: open under another worker) into slideNNN/result.txt, and run
# PIL-first adjudication (rejudge_adjudicate.py) for any FAIL leg that has no
# banked adjudicate_fresh_*.txt yet. Idempotent; never deletes transcripts.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$RJ/fresh_collect_018034.log

clean() { # file -> PASS|FAIL|NORESULT
  local f=$1
  [ -f "$f" ] || { echo NORESULT; return; }
  grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f" || { echo NORESULT; return; }
  grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)'
}
pick() { # first clean among args -> "VERDICT path" (relative) or "NORESULT -"
  local v f
  for f in "$@"; do
    v=$(clean "$f")
    if [ "$v" != NORESULT ] && [ -n "$v" ]; then echo "$v ${f#$ROOT/}"; return; fi
  done
  echo "NORESULT -"
}
title_of()  { sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=$((10#$1));" 2>/dev/null | head -1; }
region_of() { python3 "$RJ/pick_dense_region.py" "$1" 2>/dev/null | awk '{printf "%s,%s-%s,%s", $1,$2,$3,$4}'; }

SCOPE="018 019 020 021 022 023 024 026 027 028 029 030 031 032 033 034"
for N in $SCOPE; do
  D=$RJ/slide$N; NN=$((10#$N))
  read -r FV FP <<< "$(pick "$D/judge_full_fresh.txt" "$D/judge_full.txt" "$D/judge_full_retry.txt" "$D/judge_full.txt.W02bank" "$D"/judge_full_*.txt "$D"/judge_full*.bak)"
  read -r BV BP <<< "$(pick "$D/crop_dense_judge_fresh.txt" "$D/crop_dense_judge.txt" "$D/crop_dense_judge_retry.txt" "$D/crop_dense_judge.txt.W02bank" "$D"/crop_dense_judge_*.txt "$D"/crop_dense_judge*.bak)"
  # carry TITLE/REGION forward from existing result.txt when present
  TITLE=$(grep -m1 '^TITLE=' "$D/result.txt" 2>/dev/null | cut -d= -f2-)
  REGION=$(grep -m1 '^REGION=' "$D/result.txt" 2>/dev/null | cut -d= -f2-)
  [ -n "$TITLE" ] || TITLE=$(title_of "$N"); [ -n "$TITLE" ] || TITLE="slide $N"
  [ -n "$REGION" ] || REGION=$(region_of "$N"); [ -n "$REGION" ] || REGION="?"
  [ "$FP" = - ] && FP=${D#$ROOT/}/judge_full.txt
  [ "$BP" = - ] && BP=${D#$ROOT/}/crop_dense_judge.txt
  cat > "$D/result.txt" <<EOF
SLIDE=$N
TITLE=$TITLE
RENDER=${D#$ROOT/}/render.png
REGION=$REGION
FULL=$FV
CROP=$BV
FULL_TRANSCRIPT=$FP
CROP_TRANSCRIPT=$BP
EOF
  if [ "$FV" = FAIL ] && [ ! -s "$D/adjudicate_fresh_full.txt" ]; then
    python3 "$RJ/rejudge_adjudicate.py" "$N" --full > "$D/adjudicate_fresh_full.txt" 2>&1
    echo "$N FULL=FAIL adjudicated -> adjudicate_fresh_full.txt $(date -u +%FT%TZ)" >> "$LOG"
  fi
  if [ "$BV" = FAIL ] && [ ! -s "$D/adjudicate_fresh_crop.txt" ]; then
    python3 "$RJ/rejudge_adjudicate.py" "$N" --crop > "$D/adjudicate_fresh_crop.txt" 2>&1
    echo "$N CROP=FAIL adjudicated -> adjudicate_fresh_crop.txt $(date -u +%FT%TZ)" >> "$LOG"
  fi
  echo "$N FULL=$FV CROP=$BV $(date -u +%FT%TZ)" >> "$LOG"
done
echo "collect done $(date -u +%FT%TZ)" >> "$LOG"
