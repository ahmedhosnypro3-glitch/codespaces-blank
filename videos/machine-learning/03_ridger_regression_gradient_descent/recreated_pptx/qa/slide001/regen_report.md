# regen_report.md — slide 001, deck `machine-learning/03_ridger_regression_gradient_descent`

Worker: `regen-s001` · Run date: 2026-10-23 · Run type: REGENERATION (no re-judge)

## Scope

Slide 001 was previously judge-certified (attempt 1, banked transcripts below) but its
PPTX deliverable was MISSING from this workspace. This run regenerated the deliverable
from the banked build script and re-rendered it. **NO visual re-judging was performed** —
the banked judge transcripts remain the accepted verdicts.

## What was regenerated

1. **Asset restored** — `recreated_pptx/build/assets/logo_slide001.png` (297×77 px, 72dpi)
   was absent from `build/assets/` (only the three `eq_*.json` sidecars for slides 009/023
   were present), which made `build/slide_001.js` un-runnable as-is. Restored per the
   script's own header notes: an exact crop of `unique_slides/slide_001.jpg` at
   x592..888, y456..532 (the build script's documented geometry). Verified: the extracted
   asset vs the source crop is **0 px diff** (identical bytes in RGB), and vs the embedded
   copy inside the built pptx it is also 0 px diff.
2. **PPTX built** with the existing script, unmodified:
   `NODE_PATH=$(npm root -g) node recreated_pptx/build/slide_001.js`
   → `recreated_pptx/slide_001_recreated.pptx` (88163 bytes, valid zip, `unzip -t`
   clean, `ppt/media/image-1-1.png` = the restored logo).
3. **Re-rendered** from the fresh pptx with a private LibreOffice profile:
   `soffice --headless -env:UserInstallation=file://$TMPDIR/lo_slide001 --convert-to pdf`
   → `pdftoppm -png -r 150` → **`recreated_pptx/qa/slide001/render_regen.png`**
   (NEW file name; the banked `render_1.png` was NOT touched).

## Toolchain observed

- Node 26.12.1 via nvm; pptxgenjs resolved from the global NODE_PATH.
- LibreOffice 24.2.7.2; no Arial on this host — `fc-match Arial` → Liberation Sans
  (metric-compatible substitution, the same class the certified worker already
  documented as the render's residual variance).

## House-chrome check

`shared_patterns/house_chrome_check.py qa/slide001/render_regen.png 1`

```
HOUSE CHROME CHECK: PASS (panel x 112-1882, y 94-bottom; strokes L/R/bottom present,
top bare; badge center (1824,152) d=68; all within tol 8)
```

## Render delta vs the banked render (documented, not a gate)

`render_regen.png` vs banked `render_1.png`: 42821 of 2251125 px differ >8 (1.90%),
max diff 233, spread across every text band plus the logo band. Localized and
attributed:

- Logo asset inside the new pptx is byte-identical to the source crop and to the
  banked component → the logo's own pixels are not the source of the band delta; the
  delta is the PPTX-internal PNG **re-encode** differing between pptxgenjs/zlib
  versions on the two build hosts (same source pixels, different compressed bytes).
- Text bands: Arial → Liberation Sans substitution on this host shifts
  antialiasing/advance rounding on every run of glyphs, which is the documented
  residual variance for this deck's renders (2–8% advance-width jitter).

Consequences: chrome, positions, colors, and content are unchanged; the certification
recorded by the banked judges still stands (see the transcripts below). No rebuild.

## Banked judge transcripts verified present (NOT re-judged)

All five attempt-1 winner bodies exist under
`videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide001/`
and each ends in a PASS verdict:

| Leg | Transcript | Verdict |
|---|---|---|
| A — full-slide | `judge_attempt_1.txt` | PASS — zero discrepancies, zero visual-quality defects |
| B — crop `title` | `crop_1_title_judge.txt` | PASS (MINOR: red saturation) |
| B — crop `preparedby` | `crop_1_preparedby_judge.txt` | PASS (MINORs: italic substitution) |
| B — crop `instructors` | `crop_1_instructors_judge.txt` | PASS (MINORs: italic header) |
| B — crop `logo` | `crop_1_logo_judge.txt` | PASS (MINORs: artifact class) |

Supporting evidence also verified present: `build_attempt_1.js` (byte-identical to
`build/slide_001.js`, md5 `b57177d0fa089828d36a16774e623caa` on both), `render_1.png`,
`cut_crops.py`/`cut_crops.txt`, `crop_verdicts_1.txt`, `worker_report.md`,
`selfcheck_measure_original.txt`.

## DB state (left as certified)

- `gen_status=passed`, `visual_check=PASS` — both already correct and left unchanged.
- `pptx_path` / `build_script` already pointed at `recreated_pptx/slide_001_recreated.pptx`
  and `recreated_pptx/build/slide_001.js`; no write was needed.
- Liveness: `claim`/`heartbeat`/`release` used correctly (`release 1 worker=regen-s001`),
  then `set 1 gen_status passed --worker regen-s001` to restore the field the claim
  had flipped to `building`. Final row: `(1, passed, PASS, <pptx_path>, <build_script>, '', None)`.

## Nothing left in progress

Deliverable exists, is a valid zip, re-renders, and passes the house-chrome check.
Asset restoration was the only missing piece. No re-judge, no certified-component edits.
