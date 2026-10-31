# merge_gate_plan.md — S9 merge-gate dry run (PREP ONLY, 2026-10-31)

Read-only gate-prep. No git, no deletions, no deck/DB/pptx modifications. All paths below
are absolute. NS = `/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent`,
D = `$NS/recreated_pptx/build/final_deck`, RJ = `$NS/recreated_pptx/qa/rejudge_20261027`.

## 1. Inspection results (measured 2026-10-31)

### 1.1 `$D` contents
- `final_deck_tool.py` (14 KB) — continuous final-deck tool. Subcommands:
  - `verify-structure` — fail-loud OPC check: deck exists, `ppt/slides/slide1..51.xml` all present, skeleton parts md5-checked.
  - `init-ledger` — writes `final_deck_state.json` (all pages placeholder).
  - `update <pages...>` (ascending) — MODE=update N: replaces page N with certified `slide_NNN_recreated.pptx` content at OPC package level (slide XML verbatim, rels retargeted, media renamed per slide), atomic temp+rename, post-write self-check, appends ledger rows + banks deck md5. Reads the DB to confirm the page is `gen_status='passed' AND visual_check='PASS'` before updating.
  - `mark-render <pages...> PASS|FAIL <detail>` — flips `render_check` in the ledger.
  - Constants: `TOTAL=51`, `DECK=$NS/recreated_pptx/03_ridger_regression_gradient_descent_final.pptx`, `LEDGER=$NS/recreated_pptx/final_deck_state.json`.
- `render_check_pages.py` — per-update render gate. Usage: `render_check_pages.py <page> [<page>...]` (ascending ints; `--help` NOT supported, it crashes on it). Requires each page's ledger row `status == "certified"`. Renders the final deck AND each source pptx in ONE LibreOffice session (profile `scratch/tmp/s21_lo_profile_299640`, TMPDIR redirected to project scratch), checks deck PDF page count == 51, rasterizes at 150 dpi (`pdftoppm -f N -l N` for deck page N, `-f 1 -l 1` for source N), PIL-diffs — 0 differing pixels required. Writes `gate_report.txt` under `$NS/recreated_pptx/qa/final_deck_updates/gate_<stamp>_p<N...>/` with `pages/`, `src/`, `src_png/` artifacts. Exit 0 = all PASS; exit 1 = any mismatch (stop-and-fix law) and marks FAIL in the ledger.
- `make_placeholders.js`, `poll_and_update.sh`, `__pycache__/`.

### 1.2 `$NS/recreated_pptx/final_deck_state.json` structure
Top-level dict: `deck` (absolute deck path, note: `/home/ahmed/...` prefix — remap to `/home/codespace/...`), `doctrine` ("continuous final deck (founder directive 2026-10-25)"), `scope` ("S21_continuous_final_deck (run 299640)"), `total_pages` (51), `deck_md5`, `pages` (dict keyed by "1".."51"; each row `{page, status, source_pptx, source_md5, render_check, render_check_detail, updated_at}`), `events` (append-only list of `{at, action, ...}`; 197 entries at read time).

### 1.3 Final deck verification
- Deck exists: `$NS/recreated_pptx/03_ridger_regression_gradient_descent_final.pptx`, 4,807,772 bytes, mtime 2026-10-31 08:26.
- Slide count via unzip: **51** (`ppt/slides/slide1.xml … slide51.xml`).
- md5 on disk: **`872284b7f41336fddf39b84ef5ddc63e`** — equals ledger `deck_md5` (deck bytes match the ledger).
- Ledger page census at read time: `status` = certified 51/51; but `render_check` = **PASS 4 (pages 14, 19, 33, 51), FAIL 46, PENDING 1 (page 51, updated 08:26:31Z and not yet re-gated)** → 51/51 is NOT yet genuine at the render-gate level.
- `source_md5` vs on-disk per-slide pptx mismatches (8 pages): **4, 5, 10, 13, 15, 21, 25, 30** — the on-disk slide pptx changed after the page was updated (OMML wraps on 004/005/015/021/030 per `OMML_WRAP_LOG.md`; 010/013 other rebuilds; 025 under active CLOBBER). These pages must be restaged before the gate.

## 2. Preconditions for the real gate (51/51 genuine)

All must hold immediately before running the gate:
1. DB: `SELECT COUNT(*) FROM slides WHERE gen_status='passed' AND visual_check='PASS';` == **51** (currently 50 — slide 25 open).
2. Ledger: all 51 `pages[*].status == "certified"` AND all 51 `render_check == "PASS"`.
3. For every page N, ledger `source_md5` == md5 of on-disk `slide_NNN_recreated.pptx` (currently 8 mismatches).
4. On-disk deck md5 == ledger `deck_md5`.
5. No live soffice processes on the shared gate profile `scratch/tmp/s21_lo_profile_299640` (deck_gate_r25 shows full-51-page attempts dying with soffice exit 1 while ~479 vision-leg wrappers were running fleet-wide — lock contention on the shared LO profile; check with `pgrep -af 's21_lo_profile_299640'` and wait for quiescence, or the gate run must use a quiesced/private profile).

## 3. Exact command sequence for the final gate

Run from `D` with the namespace env. Steps 0–2 are the restage; steps 3–6 are the gate + banking.

```bash
NS=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent
D=$NS/recreated_pptx/build/final_deck
RJ=$NS/recreated_pptx/qa/rejudge_20261027
cd "$D"

# 0. Restage list: $RJ/restage_plan.md does NOT exist (agent-400 never wrote it —
#    verified by find/grep over $NS and project scratch). Derive the list from the
#    ledger at gate time instead:
python3 - <<'EOF'
import json, hashlib, os
NS="/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
s=json.load(open(NS+"/recreated_pptx/final_deck_state.json"))
def md5(p):
    h=hashlib.md5()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()
need=[]
for k,v in sorted(s["pages"].items(), key=lambda kv:int(kv[0])):
    n=int(k); p=v["source_pptx"].replace("/home/ahmed/Projects/ai_llm_slides","/home/codespace/ai_llm_slides")
    stale = (not os.path.exists(p)) or md5(p)!=v["source_md5"] or v.get("render_check")!="PASS"
    if stale: need.append(n)
print(" ".join(map(str,need)))
EOF
# → RESTAGE="<list>"; if $RJ/restage_plan.md is ever written by agent-400, prefer its
#   list after cross-checking against the ledger-derived list above.

# 1. Restage stale pages (OPC-verbatim update per page; DB must show the slide passed):
python3 final_deck_tool.py verify-structure          # pre-check, must pass
python3 final_deck_tool.py update $RESTAGE             # ascending page numbers

# 2. Per-update render gate on the restaged pages (one LO session per invocation):
python3 render_check_pages.py $RESTAGE                 # exit 0 = 0 px differ; retry per-page on FAIL

# 3. THE MERGE GATE (S9): full 51-page gate, merged render vs EVERY source render in
#    ONE LibreOffice session, 0/51 mismatched pages required:
pgrep -af 's21_lo_profile_299640' || echo "profile quiescent"
python3 render_check_pages.py 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51
# exit 0 + "render gate PASSED for pages [1..51]" = gate green; ledger render_check all PASS

# 4. Structure re-verify + bank md5:
python3 final_deck_tool.py verify-structure
md5sum $NS/recreated_pptx/03_ridger_regression_gradient_descent_final.pptx \
  > $NS/recreated_pptx/03_ridger_regression_gradient_descent_final.pptx.md5

# 5. Bank the gate report (render_check_pages.py already wrote it under
#    $NS/recreated_pptx/qa/final_deck_updates/gate_<stamp>_p1-...-p51/gate_report.txt —
#    keep that dir as the canonical bank; copy the report path + verdict into RJ):
ls -t $NS/recreated_pptx/qa/final_deck_updates/ | head -1   # newest gate_* dir = the gate
#    append the gate dir + 0/51 verdict + deck md5 to $RJ/REJUDGE_REGISTER.md (append-only)
#    and to the final summary in $RJ/REJUDGE_SUMMARY_rNN.md

# 6. Deliverables (final set, at closeout):
#    - $NS/recreated_pptx/03_ridger_regression_gradient_descent_final.pptx   (<deck>_final.pptx)
#    - $NS/recreated_pptx/03_ridger_regression_gradient_descent_final.pptx.md5 (md5 banked post-gate)
#    - gate report: $NS/recreated_pptx/qa/final_deck_updates/gate_<stamp>_p1-...-p51/gate_report.txt
#      (0/51 mismatched pages, one-LO-session methodology) + pointer in RJ
#    - $NS/CLOSEOUT_REPORT.md — fill §5 "Final merge-gate verdict" with the gate result,
#      deck md5, gate dir; §6 OMML counts; §3 open-legs census (currently TBD skeletons)
```

Gate semantics (from `render_check_pages.py` + skill `references/patterns/final-deck-merge/example.sh`):
deck PDF page count must equal 51; page N rendered at 150 dpi from the merged deck vs page 1 of
`slide_NNN_recreated.pptx` rendered in the SAME soffice session/profile; PIL `ImageChops.difference`
`getbbox()` must be None (0 px) for all 51 → "0/51 mismatched". Any mismatch = stop-and-fix law:
fix the update path, redo the page, re-run. Never LO-resave a wrapped deck (drops OMML).

## 4. Current blockers (as of 2026-10-31 ~08:40Z)

1. **Slide 25 open** — only DB-open row: slide_id 25, `gen_status='building'`, `visual_check=''`,
   visual_attempts=4, worker `S27_019_025`. Newest clean rejudge legs: FULL FAIL
   (`judge_full_k17z3.txt` 08:16Z), CROP PASS (`crop_dense_judge_k17n.txt` 08:03Z);
   k17z2 legs still pending. Additionally `slide_025_recreated.pptx` is under ACTIVE CLOBBER
   (CLOBBER_WATCH pid 2488910 logging repeated events; md5 churn observed 07:58→08:20Z) and its
   ledger source_md5 (8a355c24…) ≠ disk (c50e78bf… at 08:20Z). Until 25 certifies clean AND the
   file stops churning, page 25 cannot be restaged or gated.
2. **OMML wraps pending** — `$RJ/OMML_WRAP_LOG.md`: 004, 005, 015, 021, 030 wrapped+replaced with
   parseable-only subset manifests (wrapper fail-loud on `\underline` / `\mathbf{\hat{Y}}` leaves
   rId1/rId2/rId4 on 004, rId7 on 005, 8 rels on 015, rId6 on 021 as plain PNG embeds);
   009/036/039 already wrapped (untouched); slide 25 untouched. `$RJ/OMML_WRAP_PLAN_r3.md` lists
   13 wrap candidates total (004, 005, 015, 021, 023, 030, 031, 032, 037, 044, 048, 050, 051) —
   031/032/037/044/048 and 050(Z1–Z3)/051(partial) need mathtext re-banked from build scripts
   before manifests; 023 needs wrapper extension or pre-transform for `\underline`.
   Every per-slide wrap changes the slide pptx bytes → its deck page must be re-`update`d and
   re-gated (8 pages already show source_md5 drift: 4, 5, 10, 13, 15, 21, 25, 30).
3. **Restage plan missing** — `$RJ/restage_plan.md` does not exist (no agent-400 artifact found
   anywhere under $NS or project scratch). The restage list must be derived from the ledger at
   gate time (step 0 above): currently 47 pages have `render_check != PASS` (46 FAIL + 1 PENDING)
   plus the 8 source_md5-mismatch pages overlap that set.
4. **Render-gate census** — ledger `render_check`: PASS only on pages 14, 19, 33, 51; FAIL 46;
   PENDING 1 (51, updated 08:26:31Z). Latest full-51 gate attempts (deck_gate_r25) all died on
   shared-LO-profile contention, not on pixel mismatches — schedule the final gate in a quiescent
   window (fleet had 479 live `vision_leg.sh` wrappers at 08:20Z).
5. **Rejudge wave still hot** — REJUDGE_SUMMARY_r34 (08:20Z): FULL PASS 28 / FAIL 23, CROP
   PASS 39 / FAIL 12, 29 slides on the open list; many FAILs carry banked PIL dismissals in
   REJUDGE_REGISTER.md. Closeout census must be re-scanned at gate time, not copied from r34.

## 5. Notes / assumptions

- `final_deck_state.json` stores paths with the `/home/ahmed/Projects/ai_llm_slides` prefix; remap
  to `/home/codespace/ai_llm_slides` when reading from this codespace (done in all snippets above).
- `render_check_pages.py` takes page numbers only (no flags); `--help` crashes it — usage is in
  its docstring (lines 1–10).
- Gate report banking location is fixed by the tool: `$NS/recreated_pptx/qa/final_deck_updates/gate_<stamp>_p*/gate_report.txt`
  — never move/delete gate dirs (evidence law); only append pointers in RJ.
- CLOSEOUT_REPORT.md at $NS root is currently a skeleton with TBD sections (§3, §5 verdict, §6);
  it is a final deliverable and gets its numbers only after the gate runs green.
