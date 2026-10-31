#!/usr/bin/env bash
# waveW4_harvest_001017.sh — after the W4 legs finish: extract per-slide
# verdicts from judge_full_w4.txt / judge_crop_w4.txt, append rows to
# REJUDGE_REGISTER.md (append-only) and write waveW4_summary.md.
# Read-only w.r.t. transcripts; never touches DB or pptx files.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027

clean() {
  local f=$1
  [ -f "$f" ] || { echo NORESULT; return; }
  grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f" || { echo NORESULT; return; }
  grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)'
}
exhausted() { # leg wrapper printed EXHAUSTED and no clean transcript
  local f=$1 w=$2
  [ -f "$f" ] || return 1
  grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f" && return 1
  [ -f "$w" ] && grep -q 'EXHAUSTED' "$w"
}

NP=0; NF=0; NE=0
{
  echo ""
  echo "## Wave W4 (rejudge 2026-10-27 wave W4, launched 2026-10-31) — slides 001-017 fresh full+crop legs on current certified bytes"
  echo ""
  echo "| slide | FULL (judge_full_w4) | CROP (judge_crop_w4) | pptx md5 | notes |"
  echo "|---|---|---|---|---|"
} >> "$RJ/REJUDGE_REGISTER.md"

: > "$RJ/waveW4_verdicts_001017.txt"
for n in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017; do
  d=$RJ/slide$n
  fv=$(clean "$d/judge_full_w4.txt"); cv=$(clean "$d/judge_crop_w4.txt")
  [ "$fv" = NORESULT ] && exhausted "$d/judge_full_w4.txt" "$d/judge_full_w4.wrapper.out" && fv=EXHAUSTED
  [ "$cv" = NORESULT ] && exhausted "$d/judge_crop_w4.txt" "$d/judge_crop_w4.wrapper.out" && cv=EXHAUSTED
  md=$(grep "slide_${n} " "$RJ/waveW4_md5_001017.txt" | tail -1 | awk '{print $2}')
  [ -z "$md" ] && md=$(md5sum "$NS/recreated_pptx/slide_${n}_recreated.pptx" | awk '{print $1}')
  case $fv in PASS) NP=$((NP+1));; FAIL) NF=$((NF+1));; EXHAUSTED) NE=$((NE+1));; esac
  echo "$n full=$fv crop=$cv md5=$md" >> "$RJ/waveW4_verdicts_001017.txt"
  n429f=0; n429c=0
  [ -f "$d/judge_full_w4.txt" ] && n429f=$(grep -ci 429 "$d/judge_full_w4.txt" || true)
  [ -f "$d/judge_crop_w4.txt" ] && n429c=$(grep -ci 429 "$d/judge_crop_w4.txt" || true)
  echo "| $n | $fv | $cv | $md | full 429=$n429f crop 429=$n429c; transcripts judge_full_w4.txt + judge_crop_w4.txt; render_w4.png 2001x1125 |" >> "$RJ/REJUDGE_REGISTER.md"
done

{
  echo "# waveW4_summary — rejudge 2026-10-27 wave W4, slides 001-017 (launched $(date -u +%FT%TZ))"
  echo ""
  echo "Fresh full (payload_A.txt) + crop (payload_B_025.txt) vision legs on the CURRENT certified"
  echo "pptx bytes (md5s in waveW4_md5_001017.txt), renders render_w4.png 2001x1125 @150dpi, crop pair"
  echo "crop_dense_render_w4.png / crop_dense_orig_w4.png via pick_dense_region.py. Legs: OCC_MAX=700"
  echo "ATTEMPTS=10 setsid nohup wrappers, 2 slides (4 legs) per wait, batches of 4."
  echo ""
  echo "## Counts (FULL leg verdicts)"
  echo ""
  echo "- PASS: $NP"
  echo "- FAIL: $NF"
  echo "- EXHAUSTED: $NE"
  echo ""
  echo "## Per-slide"
  echo ""
  echo "| slide | FULL | CROP |"
  echo "|---|---|---|"
  while read -r n fv cv md; do
    echo "| $n | ${fv#full=} | ${cv#crop=} |"
  done < "$RJ/waveW4_verdicts_001017.txt"
  echo ""
  echo "Skipped slides (already-clean judge_full_w4.txt): none at launch time (no w4 transcripts existed for 001-017)."
  echo "No DB writes, no pptx modifications, no git, no evidence deleted."
} > "$RJ/waveW4_summary.md"

echo "harvest done: PASS=$NP FAIL=$NF EXHAUSTED=$NE"
