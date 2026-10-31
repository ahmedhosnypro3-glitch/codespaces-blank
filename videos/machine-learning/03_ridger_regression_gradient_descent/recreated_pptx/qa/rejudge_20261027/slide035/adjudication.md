# slide035 — FULL-leg FAIL adjudication (2026-10-31, fresh worker W01, PIL-first)

Transcript: `judge_full.txt` (clean, no 429; leg via `vision_leg.sh` t=1200 payload_A,
driver `driver_W01.log`) — FINAL VERDICT: FAIL.
Claims: MAJOR #1 title-block leading/line-spacing wider in recreation (~1.4x vs orig
~1.1-1.2x); MAJOR #2 resulting vertical placement/block distribution; MINOR blue
subtitle tone. No BLOCKER; no missing elements claimed.

Evidence (read-only PIL, slide space 960x540; render 2001x1125 scale 2.0844/2.0833;
`adjudicate_w01_full.txt` = `rejudge_adjudicate.py 035 --full`: 98,097 diff px (4.358%),
densest cells spread across glyph bands, no localized missing block; ink-only-in-original
39,405 px = handwriting heavier than typed; `adjudicate_w01_full_pil.txt`):

- Full-frame ink bands (x60-900), orig vs render (slide-space y):
  title 55.0-92.0 vs 54.2-91.2; body 176.0-220.0 / 255.0-298.0 / 327.0-365.0 vs
  179.0-220.8 / 256.3-298.1 / 329.8-365.3 — every band within 3.5 slide px.
- Title line tops orig 55/70 vs render 54.7 — same two-line block, same pitch.
- The blue subtitle "(Problem Formulation)" sits at y327-365 in the ORIGINAL
  (blue core (14,0,191)) and y330-366 in the render (core (0,0,255) = 0000FF) — the
  judge misread it as a third tightly-packed title line; the orig band at y148-164
  is ~6-12 JPEG-noise px/row spanning the full width (median ~(180,152,158)),
  not a text line, and has no counterpart claim in the analysis verbatim
  (`analysis/slide_035_final.json` bullets = title + "(Problem Formulation)" only).
- Build `build/slide_035.js:47-84` places L1/L2/subtitle at measured orig geometry
  (baseline pitch 77.5px etc.); render matches.

Disposition: both MAJORs REFUTED by pixels (all content bands within 3.5 slide px;
no block missing). MINOR subtitle tone = house 0000FF vs JPEG-diluted orig — ground-rule
class. FULL = PASS (FAIL dismissed). CROP = PASS (`crop_dense_judge.txt`, t=600
payload_B_035). Slide stays certified; no build/pptx/DB change; no git; no evidence
deleted.
