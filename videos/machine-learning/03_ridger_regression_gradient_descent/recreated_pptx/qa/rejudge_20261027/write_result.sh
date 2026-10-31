#!/usr/bin/env bash
# write_result.sh NNN — write slideNNN/result.txt from the clean banked transcripts.
# usage: write_result.sh NNN [note]
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
N=$1; NOTE=${2:-}
D=$RJ/slide$N; NN=$((10#$N))
clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
pick() { local f; for f in "$@"; do if clean "$D/$f"; then echo "$f"; return 0; fi; done; return 1; }
verdict() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$D/$1" | tail -1 | grep -oE 'PASS|FAIL'; }
ts() { stat -c %y "$D/$1" | cut -d. -f1 | sed 's/ /_/'; }
FT=$(pick judge_full_fresh.txt judge_full.txt judge_full_retry.txt) || FT=""
CT=$(pick crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt) || CT=""
FV=NOVERDICT; CV=NOVERDICT; FTS=""; CTS=""
[ -n "$FT" ] && { FV=$(verdict "$FT"); FTS="$(ts "$FT") UTC (clean, no 429)"; }
[ -n "$CT" ] && { CV=$(verdict "$CT"); CTS="$(ts "$CT") UTC (clean, no 429)"; }
TITLE=$(sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=$NN;" 2>/dev/null | head -1)
[ -n "$TITLE" ] || TITLE="slide $NN"
REGION=$(python3 "$RJ/pick_dense_region.py" "$N" 2>/dev/null | awk '{printf "%s,%s-%s,%s", $1,$2,$3,$4}')
[ -n "$REGION" ] || REGION="crop_dense pair (see crop_dense_render/orig.png)"
{
  echo "SLIDE=$N"
  echo "TITLE=$TITLE"
  echo "RENDER=$RJ/slide$N/render.png"
  echo "REGION=$REGION"
  echo "FULL=$FV${NOTE:+ ($NOTE)}"
  echo "CROP=$CV"
  echo "FULL_TRANSCRIPT=$D/${FT:-none}"
  echo "CROP_TRANSCRIPT=$D/${CT:-none}"
  echo "FULL_VERDICT_TS=$FTS"
  echo "CROP_VERDICT_TS=$CTS"
  echo "WRITTEN=$(date -u +%FT%TZ) fresh worker W03 (rejudge_20261027 wave, 2026-10-31)"
} > "$D/result.txt"
echo "result.txt $N: FULL=$FV ($FT) CROP=$CV ($CT)"
