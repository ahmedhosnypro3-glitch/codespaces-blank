#!/usr/bin/env bash
# docparse_refresh.sh — re-run the doc-parse crop cascade for slides whose earlier run
# completed with the chat adjudicator DOWN (deterministic-only crop decisions).
# The chat lane is live now, so those slides get a real adjudicated cascade.
# Banked evidence is never overwritten: the prior run dir is ARCHIVED first.
set -uo pipefail

VIDEO_DIR="/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
P="/home/codespace/.pyenv/versions/3.15.2/bin/python3"
SKILL="/home/codespace/.agents/skills/doc-parse"
DP="$VIDEO_DIR/pool_run/docparse"
ARCH="$DP/_archive"
LOG="$DP/refresh.log"
STAMP=$(date +%Y%m%d-%H%M%S)
MAXPAR=4

log() { echo "[$(date '+%F %T')] $*" >>"$LOG"; }

needs_refresh() {
  local num="$1" padded mf deg
  padded=$(printf '%03d' "$num")
  mf="$DP/slide${padded}/manifest.json"
  [ -f "$mf" ] || return 0
  deg=$("$P" -c "
import json,sys
try:
    m=json.load(open(sys.argv[1]))
    d=m.get('degraded') or {}
    print('yes' if d.get('chat') else 'no')
except Exception:
    print('yes')
" "$mf" 2>/dev/null)
  [ "$deg" = "yes" ]
}

refresh_one() {
  local num="$1" padded frame dest rc deg
  padded=$(printf '%03d' "$num")
  frame="$VIDEO_DIR/unique_slides/slide_${padded}.jpg"
  [ -f "$frame" ] || frame="$VIDEO_DIR/unique_slides/slide_${padded}-.jpg"
  if [ ! -f "$frame" ]; then log "slide $num: FRAME NOT FOUND"; return 1; fi
  dest="$DP/slide${padded}"
  if [ -d "$dest" ]; then
    mkdir -p "$ARCH"
    if ! mv "$dest" "$ARCH/slide${padded}_${STAMP}" 2>>"$LOG"; then
      log "slide $num: ARCHIVE FAILED (prior run left in place)"; return 1
    fi
    log "slide $num: archived prior run -> _archive/slide${padded}_${STAMP}"
  fi
  mkdir -p "$dest/fullframe"
  "$P" "$SKILL/scripts/parse_document.py" "$frame" -o "$dest/fullframe" --timeout 150 >>"$LOG" 2>&1
  "$P" "$SKILL/scripts/crop_cascade.py" "$frame" \
    --prompt-file "$SKILL/references/prompts/crop_decision.md" \
    --out "$dest" --max-retries 3 --max-parallel 4 --max-crops 16 --max-parse-calls 24 \
    --max-depth 6 --parse-timeout 150 --chat-timeout 60 >>"$LOG" 2>&1
  rc=$?
  deg=$(grep -o '"chat": *[a-z]*' "$dest/manifest.json" 2>/dev/null | head -1)
  log "slide $num: cascade exit=$rc degraded_flag=[$deg] elements=$(grep -o '"elements": *[0-9]*' "$dest/manifest.json" 2>/dev/null | head -1)"
  return 0
}

log "=== refresh wave start (chat lane live) ==="
RUNNING=0
REFRESHED=0; SKIPPED=0; FAILED=0
for num in $(seq 1 37); do
  if needs_refresh "$num"; then
    while [ "$RUNNING" -ge "$MAXPAR" ]; do sleep 3; RUNNING=$(jobs -rp | wc -l); done
    refresh_one "$num" &
    RUNNING=$(jobs -rp | wc -l)
    REFRESHED=$((REFRESHED+1))
    log "slide $num: refresh DISPATCHED (inflight=$RUNNING)"
  else
    SKIPPED=$((SKIPPED+1))
  fi
done
wait
log "=== refresh wave done: dispatched=$REFRESHED skipped_live=$SKIPPED ==="

# Bank a coverage register: per slide, composed path + chat-degraded flag + element count.
"$P" - <<'PY' >>"$DP/refresh_coverage.md" 2>&1
import json, pathlib
DP = pathlib.Path("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/pool_run/docparse")
print("# doc-parse coverage register (post-refresh)\n")
print("| slide | chat-degraded | parse_calls | elements | composed bytes |")
print("|---|---|---|---|---|")
bad = []
for n in range(1, 38):
    d = DP / f"slide{n:03d}"
    mf = d / "manifest.json"
    comp = sorted(d.glob("composed/*_composed.md"))
    if not mf.exists():
        print(f"| {n} | NO-RUN | - | - | - |"); bad.append(n); continue
    m = json.load(open(mf))
    deg = "yes" if (m.get("degraded") or {}).get("chat") else "no"
    st = m.get("stats", {})
    nbytes = comp[0].stat().st_size if comp else 0
    if deg == "yes": bad.append(n)
    print(f"| {n} | {deg} | {st.get('parse_calls','?')} | {st.get('elements','?')} | {nbytes} |")
print(f"\nSlides still chat-degraded or missing: {bad if bad else 'NONE'}")
PY
log "coverage register written: $DP/refresh_coverage.md"
echo "refresh wave complete (see $DP/refresh_coverage.md)"
