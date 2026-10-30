# Worker report — slide 040 "Training of Linear Regression Model"

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent`
Worker: `worker_slide040_r2` (claim taken over with `--force` from the stale
`worker_slide040_1792763317`; heartbeat refreshed at re-establish).

## Deliverable

| Field | Value |
|---|---|
| pptx | `recreated_pptx/slide_040_recreated.pptx` (single plain-named deliverable) |
| build script | `recreated_pptx/build/slide_040.js` (md5 `059589927e99c454cf85a9e6e1fcf1ad`) |
| render | `recreated_pptx/qa/slide040/render_3.png` (2001×1125 = 150dpi, 13.33×7.5in) |
| build attempts banked | 1, 2, 3 (`qa/slide040/build_attempt_{1,2,3}.js`) |
| final status | PASS — all legs |

## Build history

- **Attempt 1 — FAIL** (`qa/slide040/judge_attempt_1.txt`, verdict line present).
  Root cause: one 760px text box for all three lines. 760px is exactly the 44pt
  Arial-bold advance of the title (verified via Liberation Sans Bold
  `getlength(...) * 44/100 = 760`), so the title wrapped into
  "Training of Linear Regression" + "Model" — 4 red bands instead of 2
  (confirmed by `scratch/measure040/adjudicate_wrap.py`).
- **Attempt 2 — no certifiable verdict.** The judge body was coherent and confirmed
  the wrap fix (per-line wrap-safe widths 850/240/380) but was **truncated with no
  `FINAL VERDICT:` line**, so it is not certifiable evidence. Its three findings
  were PIL-adjudicated (below) and one was confirmed-applied in attempt 3.
- **Attempt 3 — PASS.** Adds the original's **double space** between "of" and
  "Linear": `centeredLine("Training of  Linear Regression Model", 44, 474, 177, RED, 850)`.
  Live script and banked `build_attempt_3.js` are **byte-identical** (whole-file
  diff clean).

## Verification performed on attempt 3

- Chain fresh: `build/slide_040.js` 22:42:27 → `slide_040_recreated.pptx` 22:42:27 →
  `render_3.png` 22:42:31.
- `shared_patterns/house_chrome_check.py render_3.png 40` →
  **PASS** (panel x112–1882 y94–bottom; strokes L/R/bottom present, **top bare**;
  badge center (1824,152) d=68; all within tol 8).
- `selfcheck_attempt_3.py` (red/blue masks patched to exclude the house strokes and
  the purple badge ring — the first version's counts were contaminated) →
  **SELF-CHECK: PASS**, output banked at `qa/slide040/selfcheck_attempt_3_output.txt`.
  Key numbers:
  - frame containment: 0px ink outside the panel
  - red text bands = 2 (single-line title w768 ctr471; 'Solved Example' w335 ctr461)
  - blue 'usnig SGD' y257..291 ctr472 (inside the title-block region)
  - badge delta dx −1.2 / dy −0.8 frame px
  - title interior gaps original `[15,25,13,16]` vs render `[16,27,15,17]` —
    **max per-gap deviation 1.9 frame px**
  - background: white margin (255,255,255) + E9E9E7 panel (233,233,231) — house chrome

## Judge legs for attempt 3 (all PASS)

| Leg | Type | Payload | Transcript | Verdict |
|---|---|---|---|---|
| Full slide | Template A | `judge_payload_2.txt` (byte-identical to frozen `shared_patterns/judge_protocol_03.md`) | `qa/slide040/judge_attempt_3.txt` | **PASS**, zero discrepancies |
| title_block | Template B crop-pair | `crop_payload_2.txt` (matches frozen crop payload, `NNN`→`040`) | `qa/slide040/crop_3_title_block_judge.txt` | **PASS**, no defects |
| blue_line | Template B crop-pair | `crop_payload_2.txt` | `qa/slide040/crop_3_blue_line_judge.txt` | **PASS**, no defects |

All three transcripts contain a real `FINAL VERDICT:` line. Dispatches went through
`scripts/16_vision_gate.sh` with `--thinking high --max-tokens 65536 --timeout 600`,
one call at a time. Prompts banked as `judge_prompt_3.txt`,
`crop_prompt_3_title_block.txt`, `crop_prompt_3_blue_line.txt`.

Full-slide transcript confirms verbatim text including the preserved original typo
"usnig", matching centered three-line stack red/blue/red, matching frame strokes
(L/R/bottom, no top), yellow '40' badge, no tables/charts/diagrams/images missing,
no overflow/clipping/collisions. The bottom-center pointer is a video-capture
artifact and is correctly omitted per ground rule (c).

Crop pairs were cut at **matched effective scale** (both sides upscaled to identical
pixel size; `Sx=2001/960`, `Sy=1125/540`): title_block bbox 85,166..858,376
(1612×439), blue_line 359,240..589,300 (480×126), badge 850,47..904,101 (114×114).

## PIL adjudication of the attempt-2 findings

Banked at `scratch/measure040/adjudicate_attempt3.py`.

1. **Double space after "of"** → **CONFIRMED AND APPLIED.** Original interior
   word-gap 25px against single-space neighbours 13–16px; attempt 3 reproduces it
   (27px render vs 25px orig, 1.9px max per-gap deviation across all four gaps).
2. **"Badge ~35px too low"** → **REFUTED by measurement.** Render disc centroid
   (875.3, 72.7) frame px vs original (876.5, 73.5) — delta dx −1.2 / dy −0.8px,
   far inside the 4px tolerance. The judge's "y116 vs y80" was a scale-confused eye
   estimate (450dpi-scale numbers compared against 150dpi-frame numbers).
3. **"Background should be F2F2F2"** → **REFUTED.** The original is a white outer
   margin + E9E9E7 gray panel — exactly the deck house chrome that GROUND RULES (a)
   declares intentional (measured `qa/slide040/selfcheck_attempt_3_output.txt` §9).
   Attempt 3 matches it.

## DB state at close

- `gen_status=passed`, `visual_check=PASS`, `visual_attempts=3`,
  `visual_transcript=recreated_pptx/qa/slide040/judge_attempt_3.txt`,
  `pptx_path=recreated_pptx/slide_040_recreated.pptx`,
  `build_script=.../recreated_pptx/build/slide_040.js`,
  claim released (`worker_slide040_r2`).

## Notes / debt

- No equations, tables, or charts on this slide, so no OMML wrap or graphgen work
  applies.
- The pointer icon at (508,470) in the original is 1–2 dark px — a video-capture
  cursor artifact, correctly omitted.
- Web-source research leg: not run in this window (research is interleaved and never
  build-gated per the deck AGENTS.md; no `sources/slide_040_source/SOURCES.md`).
