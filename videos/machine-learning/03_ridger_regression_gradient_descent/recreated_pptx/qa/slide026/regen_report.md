# REGEN REPORT — slide 026 "Gradient Descent Solution" (deck 03, machine-learning/03_ridger_regression_gradient_descent)

**Worker:** `w26-regen-20261023` — 2026-10-23.
**Operation:** deliverable regeneration ONLY. The prior lane (worker `w26-r3-20261021T0538`,
2026-10-21) certified this slide (`gen_status=passed`, `visual_check=PASS`,
`visual_attempts=5`), but the banked PPTX deliverable was MISSING from the workspace
(only the banked `slide_026_recreated.pdf` render survived). Per the dispatch: NO re-judge —
the banked judge transcripts are the accepted verdicts. Nothing in the certified build was
edited in place; the banked build script was run as-is.

## 1. What was regenerated

- **Build command** (run from the project root, exactly as dispatched):
  `NODE_PATH=$(npm root -g) node videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_026.js`
- **Result:** `wrote slide_026_recreated.pptx` — the script's first run in this workspace
  succeeded with no errors. The script self-contained: it requires only `pptxgenjs` (global
  NODE_PATH) and `../../shared_patterns/house_chrome.js` (present). No asset PNGs, no
  `render_eq.py` equations (spec `equations: []`), no graphgen images — no restoration of any
  missing asset was needed.
- **Deliverable:** `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_026_recreated.pptx`
  (65,324 bytes; single plain-named version; no suffixes).
- **Validity:** `unzip -t ...slide_026_recreated.pptx` → "No errors detected in compressed data."
  (all 30 entries OK: [Content_Types].xml, docProps, 1 slide + rels, slideLayout/Master, theme, notesMaster.)

## 2. Re-render (own LibreOffice profile)

- Private profile under project scratch:
  `soffice --headless -env:UserInstallation=file:///workspaces/codespaces-blank/ai_llm_slides/scratch/tmp/lo_slide026 --convert-to pdf --outdir $TMPDIR videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_026_recreated.pptx`
- `pdftoppm -png -r 150` → copied to
  `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026/render_regen.png`
  (2001×1125, 168,572 bytes).
- **HOUSE CHROME CHECK: PASS** — `python3 videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/house_chrome_check.py qa/render_regen.png 26`:
  "panel x 112-1882, y 94-bottom; strokes L/R/bottom present, top bare; badge center (1824,152) d=68; all within tol 8"
  (no top stroke — as required for this deck).

## 3. Optional comparison vs banked evidence (recorded, NOT a judgement)

Both renders at 150 dpi, 2001×1125, diffed with an identical predicate (per-channel |Δ|>0):

- **vs the banked PDF render** (`recreated_pptx/slide_026_recreated.pdf`, itself re-rendered to PNG for the diff):
  **135,478 differing pixels (6.02% of 2,251,125)**.
- **vs the banked certified render** (`qa/slide026/render_9.png`, the render the 2026-10-21
  judge legs scored, md5 `b3a5b9e0082de44df247474ff40679ce`):
  **76,866 differing pixels (3.41%)**.
- Diff bbox (both comparisons): frame **y61..491, x109..885** = exactly the text bands
  (title, GD header, rowA–rowD, Notes header, N1–N4). The gray panel, the red L/R/bottom
  strokes, the blue content-box border and the badge are PIXEL-IDENTICAL (zero diffs in those
  regions). Magnitudes spread antialiasing-style (median 55, p95 255).
- Conclusion recorded, not adjudicated: glyph-level rasterization jitter from a second
  LibreOffice render session; no content, geometry, color or chrome change. The build script
  was not edited, so the composition is byte-equivalent in intent to the certified build.

## 4. Judgement explicitly NOT re-run

Dispatch law: the DB already carries `visual_check=PASS` (`visual_attempts=5`) and
`gen_status=passed`; the banked transcripts below ARE the accepted verdicts. No vision call
was made by this worker; no lane was re-opened.

**Banked judge transcripts verified present (paths, all under `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026/`):**

| Transcript | Leg | Verdict |
|---|---|---|
| `judge_attempt_5.txt` (3,467 B, 2026-10-21 06:27) | Template A full-slide on render_9 | **PASS** — "None at BLOCKER, MAJOR, or MINOR severity"; "FINAL VERDICT: PASS — faithful, usable recreation." |
| `crop_9_notes_judge.txt` (2,462 B, 2026-10-21 06:31) | Template B zoomed notes crop | **PASS** — "None identified in this region"; "FINAL VERDICT: PASS" |
| `crop_7_alg_judge.txt` (1,872 B, 2026-10-21 04:26) | Template B zoomed alg crop (render_7; region unchanged since — see change-isolation proof in `worker_report.md`) | **PASS**, one MINOR PIL-refuted by `adjudication_a7_algcrop.md` |
| `adjudication_a7_algcrop.md` (2,140 B, 2026-10-21 04:58) | PIL-first refutation of the alg-crop MINOR | three-ground refutation (pptx XML run audit: no rowA underline exists; no bar in either image's band; cited crop region contains no stroke) |

Supporting banked evidence also intact and untouched: `render_1..9.png`, `build_attempt_1/3/4.js`,
`judge_attempt_1..4.txt`, `selfcheck_attempt_*.py/.out`, `probe_*.out`, `measure_frame*.py/_out.txt`,
`house_chrome_9.txt`, and the banked PDF `recreated_pptx/slide_026_recreated.pdf` (still present,
NOT deleted — note the PDF is banked evidence, not the deliverable).

## 5. CARRIED-FORWARD MINOR-vs-frame deviations

Recorded, measured, and still present because this regen ran the certified build script
AS-IS. Source: `qa/slide026/handover_w8_026_2026-10-21.md` §3a/§3b/§3c (that file's top
STATUS UPDATE classifies these as a banked record of three MINOR-level emphasis differences
between the certified build and the original frame, kept for any future rework — a fix would
require a re-render + re-judge under the founder's single-version rule; nothing authorises
editing the certified pptx in place).

1. **MINOR-1 — rowA weight.** The original prints "[1] Start with initial Random Weights (W)"
   with "Random Weights (W)" in REGULAR weight (same-line composition-controlled density:
   Random 1.11x, Weights 0.92x of the line's regular mean; ink widths 63/62 = Arial 17.5pt
   regular, 8-9px short of bold). The build draws it **bold** (`build/slide_026.js` rowA run
   `r("Random Weights (W)", { ..., bold: true })`).
2. **MINOR-2 — rowA underline rule.** The original carries a PALE light-blue hand-drawn rule
   under "…dom Weights" (x315..434, rows y159..160, RGB ≈ (158,155,198); B−G ≈ +41 — a
   different class from the deck's full-strength blue font underlines at B−G +106..142; bar is
   continuous across the inter-letter gap x366..380 = a rule, not glyph bottoms). There is NO
   rule under "(W)" (x439+) and none under "Start with initial". The build draws **no
   underline on rowA at all**. (Note for any future rework: the attempt-7 judge MINOR claiming
   the opposite direction — that the RENDER adds an underline — was refuted in
   `adjudication_a7_algcrop.md` with a predicate (`sum < 430`) blind to the pale rule; the
   handover's re-probe `handover_probe_rowA_final.out` stands as the recorded evidence.)
3. **MINOR-3 — rowD bold scope.** The original prints "gradient is " BOLD inside the
   underlined span (same-word ruler: the underlined "is" reads 1.48x denser at thr430 than the
   tail's regular "is"; "gradient" ink 69px = Arial bold advance exactly). The build draws
   "gradient is " REGULAR (only "almost zero" is bold), both underlined
   (`build/slide_026.js` rowD runs).

Adjudicated-REFUTED items from the same handover (do NOT re-add): title underline, red-tail
underline on "AKA Learning Rate", italic on "approximatly", bold on "negative gradient"
(keep), bold on "variable number of steps" (keep regular) — see handover §3d/§3e.

## 6. DB state (after this run)

`VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py get 26`:
`gen_status=passed`, `visual_check=PASS`, `visual_attempts=5`,
`pptx_path=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_026_recreated.pptx`,
`build_script=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_026.js`,
`visual_transcript` unchanged (the three legs listed in §4). Claim released with
`release 26 w26-regen-20261023` at the end of this run.
