# CLOSEOUT_CHECKLIST — 08_performance_measure 0/37 merge gate

State at 2026-10-31 (ledger-hygiene lane): 7/37 pages certified — pages 1, 3, 9,
20, 27, 28, 29 (`final_deck_ledger.json` status=certified; mission.db scopes
slide-1/3/9/20/27/28/29 done; both sets match exactly). 30 pages still
placeholder. verification_ledger.md slide-29 duplicate rows marked
`superseded duplicate — see row above` (append-only; no rows deleted).

## What remains before the gate can run (once 37/37 certified)

Per-slide preconditions, all 37 slides:

1. Dual-read certification per namespace AGENTS.md: `judge_attempt_K.txt` AND a
   fresh `judge_verify_K.txt` both ending `FINAL VERDICT: PASS`, original-first
   order, transcripts banked under `recreated_pptx/qa/slideNNN/`, one ledger row
   per slide in `pool_run/verification_ledger.md`.
2. `slides_progress.db` gen_status=passed + visual_check=PASS; mission.db scope
   `slide-N` done (`pool-db.sh scope-done`).
3. `final_deck_ledger.json` page N status=certified.
4. After the slide pptx's LAST byte change (OMML wrap, graph embed, any fix):
   re-run the merge update — it is idempotent and must reflect final bytes:
   `python3 pool_run/merge_final_deck.py update <N> recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx`
   (run from the namespace root; serialized by flock on `08-performance_final.pptx.lock`).

Pre-gate verification (all from namespace root):

- All 37 `recreated_pptx/slide_NNN_recreated.pptx` exist (currently 37/37 exist).
- `final_deck_ledger.json`: all 37 pages status=certified, count via
  `python3 -c "import json;d=json.load(open('final_deck_ledger.json'));print(sum(1 for p in d['pages'] if p['status']=='certified'))"` → must print 37.
- mission.db done scopes count = 37; matches certified slide set exactly
  (sqlite: on `database is locked`, sleep 5 and retry).
- No merge update in flight: `08-performance_final.pptx.lock` flock is free.

## Gate run

```
python3 pool_run/merge_final_deck.py gate 08-performance_final.pptx recreated_pptx 37
```

- Renders the merged deck and every per-slide source in ONE LibreOffice session
  (profile `recreated_pptx/.merge_gate/lo`), pdftoppm 150 dpi, pixel-diffs
  merged page N vs `slide_NNN_recreated.pptx` render. Scratch:
  `recreated_pptx/.merge_gate/`.
- PASS = prints `Mismatched pages: NONE — 0/37, merge is lossless`, exit 0.
- FAIL = exit 1 with the bad page list. For each bad page N: re-run
  `update N ...` (deck page must equal the per-slide deck bytes), then re-run
  the gate. Never hand-edit the merged pptx; never delete banked evidence.

## Post-gate closeout

1. Bank the gate output (append to a closeout log under `pool_run/`); record
   `md5sum 08-performance_final.pptx` next to the deck.
2. Confirm `recreated_pptx/.merge_gate/pages/` holds 37 rendered pages.
3. Write the closeout report: per-slide certification table (ledger rows),
   mission.db scope/task summary, gate result 0/37, final md5.
4. Ledger edits (verification_ledger.md) under `flock`; append-only — supersede
   with note-column values, never delete rows.
