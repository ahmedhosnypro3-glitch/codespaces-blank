# Slide 049 — parenthesis fix, PIL-only (attempt 15), 2026-10-26

**Founder directive (verbatim):** "slide 49 has same paranthes defect, fix it
intellijently without visual judge". NO visual-judge leg was run — this is a
PIL + deterministic-measurement certificate only. The founder's eye overrides
the att14 judge certification (`judge_attempt_14.txt`), whose PIL adjudication
(`pil_adjudication_att14.md` #3) had REFUTED the "vertical bars instead of
parentheses" finding by measuring region B (initial-W parens) instead of the
defective region A (top-table parens). Region B measured MATCH then and still
matches now; the defect was real and lived in region A.

## The defect (region A — top-table column parentheses, 12 glyphs)

The build drew the six lp + six rp tall parens around the two number rows as
**font glyphs** (`txt("(")`/`txt(")")`, fontSize 26). Measured vs the original
frame (`parenA_15.out`, render_13):

| metric | ORIG (slide_049.jpg) | RENDER_13 (before) |
|---|---|---|
| bow excursion (tip↔bow) | 2.0–3.0 px | **8.6–13.4 px** |
| stroke darkness at bow (lum min) | 118–148 | **0 (pure black)** |
| stroke | 1px thin, light gray | 2–3px bold |
| ink span | y77..107 | y70..107 (glyph box) |

## The fix

1. Gray calibration: region A's original ink signature (lum min 123,
   mean 171.8 over the bow lobes) is identical to the D-region (aug table)
   strokes that are already certified at `909090`, S=1.5 (D-region: min
   117–119, mean 172–176) — `parenA_15c.out`.
2. New Bézier class in `build/assets/gen_parens049.py`:
   `("top2", S=1.5, inkH=30.0, D=1.0, color=909090)` — same geometry family as
   the certified z49 class, distinct asset so the Z block and the top table
   never silently couple. Assets: `build/assets/parens049/paren_top2_{lp,rp}.png`.
3. `build/slide_049.js` region A: the 12 `txt()` paren calls replaced with
   `addImage` placements (same certified pattern as the Z block):
   lp x = bow − (ink_left_px·PPP + S/2); rp x = bow + 0.5 − ((ink_right_px+1)·PPP − S/2);
   y = 77 − ink_top_px·PPP; PPP = 72/600. Bow anchors = sub-pixel intensity
   centroids of the original's bow lobes (`parenA_15c.out`):
   lp [89.78, 111.18, 133.45, 155.89, 178.84, 201.21],
   rp [102.42, 124.72, 147.12, 170.07, 192.45, 214.74].

## Verification (render_15.png, 150 dpi, LO headless)

- House chrome check: **PASS** (panel, L/R/bottom strokes, no top stroke, badge).
- Closed-loop delta: render_15 vs render_13 differs in exactly one bbox —
  frame x 88..218, y 77..108 (4800 px) = region A only. No other region moved.
- Per-paren after-measurements (`parenA_15e.out`): all 12 bows within
  **±0.9 px** of the original (d_bow −0.9..+0.7); tips within 1.3 px; ink span
  y77..106/107 vs orig y77..107; stroke light gray, bowpx 1.4 vs orig 2–3 —
  same rendered signature as the certified C/D regions.
- Final deck: page 49 re-replaced from the rebuilt pptx
  (md5 `25440ad17af95627b835b34fa2382745`); deck md5
  `79286abb5452e650da75c7b52416b172`; render gate **PASS** (0 px differ,
  `qa/final_deck_updates/gate_20261026-081839_p49`).

## Evidence

- `parenA_15.py/.out` — first all-pairs sweep (row band polluted by header/tag
  ink; bows usable, tips superseded by 15e)
- `parenA_15b.out` — clean per-row traces, pair 1 (orig tip/bow/gray)
- `parenA_15c.out` — sub-pixel bow centroids + D-region gray calibration
- `parenA_15d.out` — full-frame delta map (region-A-only bbox) [trace section
  has a 2D-indexing bug; superseded by 15e]
- `parenA_15e.out` — corrected before/after per-paren table (authoritative)
- `crop_15_top2_parens_{orig,before,after}.png` — visual evidence crops
- `render_15.png` — fixed render

## Residuals (measured, within tolerance, left untouched)

- Region E (high-bracket col) / F (W-col row 1): rp ink sits 2–3 px right of
  the original (from att14-era measurements) — inside the ~4 px tolerance.
- Sibling slides that draw tall parens as font glyphs (043/045/047/050/051
  candidates) may carry the same defect class — recommend a spot check; NOT
  executed here (out of scope for this directive).
