# Restage plan — final deck 03_ridger_regression_gradient_descent (PREP ONLY, not executed)

- Prepared: 2026-10-31 by deck-prep worker. **No `final_deck_tool.py update` was run.** Per instruction, execution waits for the go-ahead.
- NS = `/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent`
- D  = `$NS/recreated_pptx/build/final_deck` (contains `final_deck_tool.py`, `render_check_pages.py`)
- Basis: `deck_md5_audit.md` (same dir) — ledger `final_deck_state.json` vs disk md5s at audit time.

## Pages needing restage (ledger source_md5 != disk md5, on-disk file is the newer certified deliverable)

Run each pair in order, from `$D`:

```bash
cd /home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/final_deck

# page 13 — rebuilt 2026-10-31 08:19Z with r18 PIL-confirmed fix (TEST-table row-label column);
# pre-fix backup md5 == ledger, so ledger is stale, disk is the fix. DB: passed/PASS.
python3 final_deck_tool.py update 13 && python3 render_check_pages.py 13

# page 4 — OMML-wrapped in place ~08:37Z (f65fd300; 1 of 4 eq rel ids wrapped, rest fail-loud skipped). DB: passed/PASS.
python3 final_deck_tool.py update 4 && python3 render_check_pages.py 4

# page 5 — OMML-wrapped in place ~08:37Z (c72f0be1; 8 of 9 wrapped). DB: passed/PASS.
python3 final_deck_tool.py update 5 && python3 render_check_pages.py 5

# page 15 — OMML-wrapped in place ~08:37Z (b6b3a99d; 1 of 9 wrapped). DB: passed/PASS.
python3 final_deck_tool.py update 15 && python3 render_check_pages.py 15

# page 21 — OMML-wrapped in place ~08:37Z (9099303f; 5 of 6 wrapped). DB: passed/PASS.
python3 final_deck_tool.py update 21 && python3 render_check_pages.py 21

# page 30 — OMML-wrapped in place ~08:37Z (c48f8fa3; 2 of 2 wrapped). DB: passed/PASS.
python3 final_deck_tool.py update 30 && python3 render_check_pages.py 30
```

Suggested order: 13 first (content fix, oldest pending), then the OMML-wrap pages 4, 5, 15, 21, 30.

## BLOCKED

```bash
# page 25 — BLOCKED until slides_progress.db shows gen_status=passed AND visual_check=PASS
# (currently: building / empty, att 4; deck page gate FAIL 19.36% px; on-disk c50e78bf != ledger 8a355c24;
#  rejudge k17z2/k17z3 legs still in flight at audit time).
# DO NOT RUN YET:
#   python3 final_deck_tool.py update 25 && python3 render_check_pages.py 25
```

## SKIP

- **Page 10** — ledger 9b4ee43a vs disk 67b341ef (stable since 2026-10-27). The pptx has no `ppt/media` at all (no eq images, 0 AlternateContent): nothing to OMML-wrap; per instruction this page is skipped, no restage command prepared.

## No action (consistent)

- Pages 14, 19, 33, 50: ledger render_check=PASS and ledger md5 == disk md5 — consistent, nothing to do.
- Page 51: ledger md5 == disk md5 (210712eb); pages-dict render_check=PENDING only because the 08:26:31Z update-page re-staged identical bytes after the 08:19:31 PASS gate — needs a re-gate only (`python3 render_check_pages.py 51`), not a restage. Optional, include if a re-gate is wanted.
- All other 42 pages: ledger md5 == disk md5.
