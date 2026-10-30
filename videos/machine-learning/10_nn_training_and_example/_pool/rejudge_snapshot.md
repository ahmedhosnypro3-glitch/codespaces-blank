# Rejudge Completeness Snapshot — scope_s1 (REPORT-ONLY)

**Frozen:** 2026-10-27 22:46:16Z · **Scope:** `scope_s1` (agent-56) · **Slides:** 21 certified
**Method:** filesystem existence checks + md5 vs ledger only. No vision calls, no builds, no fixes.
**Ledger sync** = `md5sum(recreated_pptx/build/slide_0NN_recreated.pptx)` vs `source_md5` in
`final_deck_ledger.json`. For `certified` pages `source_md5` IS the build-file md5 at merge time
(`merge_final_deck.py:153`), so a mismatch means the deck page is stale.

## Per-slide evidence (r = owning rejudge scope)

| slide | r | raw | final | render | attempts | verdict | ledger | last write |
|---|---|---|---|---|---|---|---|---|
| 001 | r1 | y | y | y | 2 | none | SYNC | 6m |
| 002 | r1 | y | y | y | 2 | none | SYNC | 6m |
| 003 | r1 | - | - | y | 1 | none | STALE | 28m |
| 004 | r2 | y | - | y | 3 | FAIL x2 | STALE | 0m |
| 005 | r2 | - | - | y | 1 | none | STALE | 29m |
| 006 | r2 | - | - | y | 1 | none | SYNC | 0m |
| 007 | r3 | - | - | y | 2 | PASS | SYNC | 20m |
| 008 | r3 | y | y | y | 2 | PASS | SYNC | 2m |
| 010 | r3 | y | - | y | 3 | none | SYNC | 3m |
| 011 | r4 | y | - | y | 2 | FAIL | SYNC | 21m |
| 012 | r4 | - | - | y | 1 | PASS | SYNC | 22m |
| 013 | r4 | - | - | y | 1 | PASS | SYNC | 24m |
| 014 | r5 | - | - | y | 3 | none | SYNC | 6m |
| 017 | r5 | y | y | y | 2 | none | SYNC | 1m |
| 018 | r5 | - | - | y | 0 | none | SYNC | 37m |
| 021 | r6 | y | y | y | 2 | FAIL | STALE | 14m |
| 022 | r6 | - | - | y | 2 | FAIL | SYNC | 17m |
| 023 | r6 | y | y | y | 2 | none | SYNC | 6m |
| 024 | r7 | y | y | y | 3 | none | SYNC | 25m |
| 026 | r7 | y | y | y | 3 | PASS | SYNC | 26m |
| 027 | r7 | - | - | y | 4 | none | SYNC | 1m |

- **render:** `qa/slide0NN/rejudge/render-1.png` present on **21/21**.
- **adjudication.md:** 0/21. **REJUDGE_REPORT.md:** 0/21.
- **verdicts:** 5 PASS (007, 008, 012, 013, 026) · 4 FAIL (004, 011, 021, 022) · 12 none.
- `raw` present 11/21 · `final` present 8/21 · ledger SYNC 17/21 (stale: 003, 004, 005, 021).

## Findings

**1. All 7 rejudge scopes are live — 0 slides stranded.**
scope_r1–r7 all `in_work` (`updated_at` 21:54:29–21:58:19, i.e. claimed ~48 min ago at freeze time;
instruction threshold is 90 min). Per-slide rejudge activity confirmed by mtimes: every slide was
written within the last 0–37 min. **No slide is stalled or abandoned.**

**2. Missing rejudge task rows (DB coverage gap, not evidence gap).**
Only r2/r6/r7 registered task rows per slide. **No task row at all for 11 slides:**
002, 003 (r1) · 007, 008, 010 (r3) · 011, 012, 013 (r4) · 014, 017, 018 (r5).
Consequence: if one of those r-workers dies, nothing in the DB records that its slides
still need a fresh render/judge/report — the run cannot self-heal. r1 has only one row
("slide_001 build script broken", task 60: `slide_001.js` uses undefined `SERIF` at ~15 call sites
→ `ReferenceError`, so slide 001's deliverable can't rebuild until fixed).

**3. Only 9 of 21 slides carry a verdict — the rest are blocked by the vision gateway.**
5 PASS (007, 008, 012, 013, 026) · 4 FAIL (004, 011, 021, 022) · 12 with no verdict. Every banked
`judge_attempt_*` for those 12 ends in an aborted vision call, not a verdict — e.g.
`qa/slide021/rejudge/judge_attempt_1.txt` ends `ABORT HangError: hard wall-clock 270s exceeded`;
`qa/slide002/rejudge/judge_attempt_1.txt` ends `Read timed out (read timeout=240)`.
Slide 018 has no judge attempt file at all. Vision-gateway instability is the single blocker.

**4. Final-deck sync — the big one.**
`final_deck_ledger.json` (22:33:20) lists all 21 certified pages, but **11 of the 21 certified pages
are wrong in the deck**, in two distinct ways (measured 22:45–22:47):
- **STALE CONTENT (4)** — deck `slideN.xml` ≠ build `slide1.xml`: **003, 004, 005, 021**. These are
  exactly the pages where the build was rewritten *after* the merge (the r-workers' fix loop).
  Their re-judge Step-6 re-merge is the sanctioned cure.
- **BROKEN IMAGES (7)** — deck XML *does* match the build, but the build's media parts are absent
  from the deck package: **001, 010, 011, 012, 014, 017, 018**. The slide is structurally correct
  yet its pictures cannot render.
- All 13 placeholder pages (9,15,16,19,20,25,28–34) also lost their full-bleed `imageN.jpg`.
- Deck totals: **24 of 34 pages have dangling media rels (73 refs)**, only 5 `ppt/media/*` parts exist.
- **Page 007 is the only repaired page** (22:44): XML matches the build *and* its 4 media were
  re-added as `page7_image-1-*.png` with rewritten rels — that is the repair pattern for the rest.
- Root cause in `merge_final_deck.py mode_update`: it skips every `ppt/media/*` when copying the
  deck forward (lines 128–129) and copies slide rels verbatim (line 137) without rewriting the
  renamed `slide{N}_*` targets, so no image in the package resolves. Merge gate will FAIL.
- **In-flight hazard:** r-workers' Step-6 re-merges run the same broken tool, so each re-judge
  "fix" re-corrupts the other pages. Apply the page-7 pattern, or fix the tool, before more merges.

**5. Storm status.** `_pool/storm_log/` shows a fleet 502/504 window ~21:00–21:20 and ongoing
vision-gateway hangs; no writes were added to `storm_log` by this scanner (no 5xx/timeout
hit my own reads). `json` parse of `final_deck_ledger.json` succeeded — no storm recovery needed.

## Banking decision (scope_s1)

**Per-slide gaps banked: 0.** All 21 slides sit in an `in_work` r-scope claimed <90 min ago with
write activity inside that window, so per the scanner rule every per-slide gap is **in-flight —
noted above, not tasked**. Specifically NOT tasked (all in-flight): missing `analysis/reanalysis`
raw/final (13 slides), missing verdict (12), missing `adjudication.md` + `REJUDGE_REPORT.md` (21),
stale ledger pages (003, 004, 005, 021 — owned by r1/r2/r6 Step-6 re-merge).

**Gaps banked: 1** — the fleet-wide final-deck sync defect. It is not a per-slide item, is owned by
no in-flight r-scope, and is actively worsening while the r-workers re-merge with the broken tool.
Already cross-referenced against existing tasks 52 and 55 (same root cause; task 55 sits in the
**failed** scope_a4 and task 52 in scope_a13, whose items are slides 22–23 only).

## Tally (frozen 22:46:16Z)

- **G = 1** gaps banked (fleet-wide deck sync; 0 per-slide — all in-flight).
- **I = 21** slides in-flight (r1–r7 all `in_work`, claimed 21:54–21:58).
- **S = 17** slides ledger-synced (stale: 003, 004, 005, 021).
- Evidence: render **21/21** · reanalysis raw 11/21 · final 8/21 · verdict 9/21
  (5 PASS / 4 FAIL) · adjudication.md 0/21 · REJUDGE_REPORT.md 0/21.

## Next actions for the orchestrator

1. **Hold further final-deck merges** until `merge_final_deck.py` is fixed or the page-7 repair
   pattern (`page7_*` media + rewritten rels) is applied to the other 23 broken pages. Every r-worker
   Step-6 re-merge currently re-corrupts the other pages.
2. **Vision gateway is the rejudge lane's bottleneck** — 12 slides have no verdict because every
   attempt aborted (HangError 270s / read timeout 240s). Retries with a wider wall are in flight.
3. **DB self-heal gap:** register task rows for 002, 003, 007, 008, 010, 011, 012, 013, 014, 017,
   018 — otherwise a dead r-worker loses those slides silently.
4. **Slide 001 cannot rebuild:** `recreated_pptx/build/slide_001.js` references an undefined `SERIF`
   (task 60) — needs an owner before slide 001 can be re-fixed.
5. `adjudication.md` + `REJUDGE_REPORT.md` are still 0/21 — the r-workers owe these per
   REJUDGE_PROTOCOL Steps 5 and 7.
