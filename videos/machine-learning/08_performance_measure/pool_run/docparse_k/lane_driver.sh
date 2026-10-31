#!/bin/bash
# docparse_k lane driver: crop-cascade slides 029-037 of 08_performance_measure.
# Isolated lane root: pool_run/docparse_k/ only. Never touches other lanes.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
LANE=$NS/pool_run/docparse_k
SKILL=/home/codespace/.agents/skills/doc-parse
LOG=$LANE/run.log
STATUS=$LANE/STATUS.md
SLIDES="029 030 031 032 033 034 035 036 037"
MAX_ATTEMPTS=6

log() { echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }

# attempt OK = exit 0 AND composed file non-empty AND every parse.json finish_reason==stop
check_ok() {
  local d=$1
  [ -d "$d" ] || return 1
  find "$d/composed" -name '*_composed.md' -size +0c 2>/dev/null | grep -q . || return 1
  python3 - "$d" <<'EOF'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1])
files = list(d.rglob('*.parse.json'))
if not files:
    sys.exit(1)
bad = 0
for f in files:
    try:
        j = json.loads(f.read_text())
    except Exception:
        bad += 1
        continue
    if j.get('finish_reason') != 'stop':
        bad += 1
sys.exit(0 if bad == 0 else 1)
EOF
}

summarize() {
  local nnn=$1 out=$2 verdict=$3
  python3 - "$nnn" "$out" "$verdict" "$LANE" <<'EOF'
import json, pathlib, sys
nnn, out, verdict, lane = sys.argv[1:5]
out = pathlib.Path(out); lane = pathlib.Path(lane)
fr = 'n/a'; cl = 0
full = sorted((out / 'full').glob('*.parse.json')) if (out / 'full').exists() else []
if full:
    try:
        j = json.loads(full[0].read_text())
        fr = str(j.get('finish_reason', '?'))
        cl = len(j.get('content') or '')
    except Exception as e:
        fr = 'err'
comp = list((out / 'composed').glob('*_composed.md')) if (out / 'composed').exists() else []
ccl = sum(len(c.read_text(errors='replace')) for c in comp)
try:
    rel = str(out.relative_to(lane))
except ValueError:
    rel = str(out)
part = lane / '.status_parts' / f'slide_{nnn}.part'
part.parent.mkdir(parents=True, exist_ok=True)
part.write_text(
    f"slide_{nnn} | {verdict} | finish_reason={fr} | full_content_len={cl} | composed_len={ccl} | out={rel}\n")
EOF
}

run_slide() {
  local nnn=$1
  local img=$NS/unique_slides/slide_${nnn}.jpg
  local base=$LANE/cascade_slide${nnn}
  local attempt=1 out rc
  [ -f "$img" ] || { log "slide $nnn MISSING INPUT $img"; summarize "$nnn" "$base" FAIL; return 1; }
  while [ "$attempt" -le "$MAX_ATTEMPTS" ]; do
    if [ "$attempt" -eq 1 ]; then out=$base; else out=$base/retry${attempt}; fi
    log "slide $nnn attempt $attempt start out=$out"
    python3 "$SKILL/scripts/crop_cascade.py" "$img" \
      --prompt-file "$SKILL/references/prompts/crop_decision.md" \
      --out "$out" --parse-timeout 300 --max-parallel 2 >> "$LOG" 2>&1
    rc=$?
    log "slide $nnn attempt $attempt exit=$rc"
    if [ "$rc" -eq 0 ] && check_ok "$out"; then
      log "slide $nnn attempt $attempt OK"
      summarize "$nnn" "$out" OK
      return 0
    fi
    log "slide $nnn attempt $attempt FAIL rc=$rc"
    attempt=$((attempt + 1))
    if [ "$attempt" -le "$MAX_ATTEMPTS" ]; then
      local s=$((120 + RANDOM % 181))
      log "slide $nnn sleeping ${s}s before attempt $attempt"
      sleep "$s"
    fi
  done
  summarize "$nnn" "$base" FAIL
  return 1
}

mkdir -p "$LANE/.status_parts"
log "driver start slides=$SLIDES max_concurrent=2 dispatch_spacing=60-90s max_attempts=$MAX_ATTEMPTS backoff=120-300s"
last_launch=0
for nnn in $SLIDES; do
  while [ "$(jobs -rp | wc -l)" -ge 2 ]; do sleep 15; done
  now=$(date +%s)
  if [ "$last_launch" -gt 0 ]; then
    want=$((60 + RANDOM % 31))
    elapsed=$((now - last_launch))
    if [ "$elapsed" -lt "$want" ]; then sleep $((want - elapsed)); fi
  fi
  last_launch=$(date +%s)
  log "dispatch slide $nnn"
  run_slide "$nnn" &
done
wait
{
  echo "# docparse_k crop-cascade lane STATUS — 08_performance_measure slides 029-037"
  echo "lane root: videos/machine-learning/08_performance_measure/pool_run/docparse_k (isolated)"
  echo "date: $(date -u +%F) | probe: pool_run/docparse_k/probe exit=0 finish=stop"
  echo "format: slide | verdict | finish_reason | full_content_len | composed_len | out"
  for nnn in $SLIDES; do
    if [ -f "$LANE/.status_parts/slide_${nnn}.part" ]; then
      cat "$LANE/.status_parts/slide_${nnn}.part"
    else
      echo "slide_$nnn | MISSING | finish_reason=n/a | full_content_len=0 | composed_len=0 | out=none"
    fi
  done
} > "$STATUS"
log "driver done"
echo "driver done"
