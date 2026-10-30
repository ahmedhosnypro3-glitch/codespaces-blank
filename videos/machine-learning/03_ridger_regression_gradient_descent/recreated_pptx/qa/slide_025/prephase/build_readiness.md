# Slide 025 — build readiness (S20b prephase pack)

Read with `prephase/delta_vs_related.md` (Δ# references its table rows).
Namespace law: `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`.

## State of the lane (verified 2026-10-25 ~15:05)

- Build: `build/slide_025.js` md5 `96f2197597b59d0f36c562922b298d47`
  (2026-10-25 08:07). Root slide — no dependency imports, no cascade.
- **Already actioned** (verified by reading the build): TL third reference line
  (y200 x88..274) + yellow caption words (LB1 "Concave", LB2 "Convex") +
  original two-line label breaks; slide-level REFLINES incl. TR pair + slanted
  strokes A/B; caption↔plot X-overlap assignment; 4 plot images placed unscaled
  at measured boxes; house chrome numeral 25 (no top stroke — correct).
- Plot generator chain: `build/generate_plots_025_k{4,5,7,8,9,10,11}.py`;
  current plots from **K10** (`plot_025_{tl,tr,bl,br}.png`). K10 already carries
  the attempt-7 crop-judge fixes (dense black wireframe, floor contour rings,
  coarse mesh, crown hue olive/green, BL annotation leaders — see its header).
- **TR crop judges FAIL** (`crop_10_tr_judge.txt`, `crop_11_tr_judge.txt`) —
  findings distilled in delta_vs_related.md §TR.

## Preconditions

- `shared_patterns/house_chrome_check.py` must PASS on the 150-dpi render
  before judging.
- Judge payloads byte-for-byte from `shared_patterns/judge_protocol_03.md`.
- Yield law while the gate is saturated: `pgrep -c -f analyze_image.py` < 8
  before any dispatch, else sleep 120.

## Build actions

- **D1 (MAJOR) TR axis handedness** — mirror the left horizontal axis
  (100→−100 top→bottom as in the original; currently reversed). Regenerate the
  TR PNG via a K11 edit of `generate_plots_025_k10.py` (axis direction /
  `invert_*` / `view_init`); re-check corner-peak emphasis after the flip
  (crop_11 item 6).
- **D2 (MAJOR) TR z=0 stroke** — remove the extra thick dark-red z=0 line the
  generator draws; the original has only the y226/y234 pair + slanted stroke A
  (those live as slide-level shapes in slide_025.js — keep them, remove only
  the in-PNG stroke).
- **D3 (MAJOR) TR spike** — raise/sharpen the central spike to z≈1.95–2.0 with
  a clean conical silhouette; remove the cyan/red diamond artifacts at its base
  (z-order/shading).
- **D4 (MINOR) TR styling** — add the faint bottom contour projection
  (`ax.contour(..., zdir="z", offset=...)`, cf. the TL rings the generator
  already draws); dotted gray gridline style; place the in-plot reference-line
  pair at z≈0.4–0.45 stopping nearer the box; trim slanted stroke A's overshoot
  past the right box edge.
- **D5 (MINOR) Label boxes** — fill 0000A0 → **#1A1A96** (dispute-1 PIL first);
  text face Arial → **serif Times-like** [?] (two instruments: prephase TL read
  + crop_9 lbl judge; settle per dispute-2 PIL / targeted re-read).
- **D6 BL/BR certificates** — no crop-judge certificates exist for BL or BR
  (legs parked). Before certification: run the two crop pairs
  (`prephase/orig_judges/crops/slide025_{bl,br}.png` vs the matching render
  crops) when a window opens. Until then BL/BR stay [?] in the cert record.
- **D7 Re-certify** — house_chrome_check 150dpi PASS → full judge
  (judge_protocol_03 payload) + zoomed crop certificates per dense region (TR
  mandatory after D1–D4; TL; BL/BR per D6; label boxes) → per-slide
  re-certification per `scripts/17_worker_instructions.md`.

## Reusable components inventory

- `shared_patterns/house_chrome.js` + `house_chrome_check.py` (deck-03 values).
- `build/generate_plots_025_k*.py` chain — K10 is current; the K5+ fix list and
  attempt-7 verdict fixes are banked in the generator headers; K11 = D1–D4.
- Advanced-graph rule: satisfied in-repo — matplotlib mplot3d + jet, no new
  dependency; images regenerate from the generator, never hand-edited.
- 022's component export pattern (`build/components/slide_022.js`) is the
  deck's precedent for exporting a certified component — 025 is root, so
  nothing to export unless a later slide builds on it.
- No `eq_*` assets needed (no equations on this slide).

## Parked legs (do not re-dispatch without a window; pgrep < 8)

- 025 full-frame read, TR crop read, BL crop read, BR crop read (crops already
  cut in `prephase/orig_judges/crops/`).
- Corroboration: lane TR judges crop_10/11 (strong, region-by-region),
  crop_9 label judges, K-chain generator headers. BL/BR least-corroborated [?].
