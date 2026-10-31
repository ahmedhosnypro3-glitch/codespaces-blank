# slide 025 FULL fresh-leg adjudication (2026-10-31 ~04:5x UTC, this worker)

Transcript: `judge_full_fresh.txt` (clean, 2026-10-31 04:33 UTC, wrapper pid 1046084,
t=1200, render.png [2026-10-31 03:37, md5 2e41bc07f2f9c969adfd81f2b4892afa] vs
unique_slides/slide_025.jpg, payload_A.txt). FINAL VERDICT: FAIL, 5 MAJOR + 2 MINOR.

PIL-first adjudication vs the NEW render (`rejudge_adjudicate.py 025 --full` ->
`adjudicate_full_fresh.txt`: 442,983 diff px = 19.68%; densest cells all in the BR
bottom band x672-816 y472-517 at 2350 px/cell; ink-only-in-render 89,713 vs
ink-only-in-original 118,482).

## MAJOR#1 BR chart type (rugged multi-valley + winding path vs smooth dome) — STANDS
Orig BR interior has 4,111 slide-px of deep-blue (basin) color; render has 32.
Render peak-color (hill) px 14,537 vs orig 8,006. The render's BR is hill/dome
dominant with the basin suppressed (k14 `Normalize(zmin-0.40*rng, zmax)` compresses
the top and the surface is 2 hills + shallow basins); the original shows a real
valley. Not refuted.

## MAJOR#2 BR bottom frame containment — CONFIRMED
BR frame bottom at slide y528.5 (red row). Render colorful surface fill runs at
full width (370-375 px/row) down to y527 — flush against the frame, 0 px margin.
Orig surface tapers to 0 colorful px at y520-525 — clear white margin before the
frame. CONFIRMED by pixels.

## MAJOR#3 BL Local/Global Minima swap — REFUTED
Build ground truth measured from the original frame (`build/slide_025.js:33-35`):
"Global Minima" ~x145..201 y439..465 (LEFT-bottom), "Local Minima" ~x286..311
y390..399 (RIGHT). Render (k14, same placement as k10-k13) puts "Global Minima"
at slide x132-177 y449-456 (LEFT) and "Local Minima" at x300-333 y456-459 (RIGHT)
(NCC 0.699 / 0.651 vs DejaVu templates); orig dark-text comps sit at x145-172 and
x310-328 in the same two spots, left label wider (27 px vs 18 px) consistent with
the longer "Global Minima" string on the left. Render matches the original; the
judge misread the original. REFUTED.

## MAJOR#4 BL red x-markers / heavier leaders — CONFIRMED (graded MAJOR/MINOR)
Render BL interior has six red comps incl. an 872-px 24x21 blob at x224-248
y372-393 plus five 4-12 px marks at the four extrema (x194-262 y358-393,
x207-245 y446-461). Orig BL interior has no such marks (only a 401-px 28x29 blob
at x188-216 y321-350 and two tiny 15-17 px specks). The red x markers are
render-added. CONFIRMED.

## MAJOR#5 TR geometry (flat square + diagonal red line vs bowl + level lines) — STANDS
Orig TR has two horizontal full-width red level lines at y222 x619-873 and
y234 x619-866 (ground truth, slide_025.js:29) — 623 slide-px red in interior.
Render TR red interior is 203 slide-px dominated by one 822-px slanted comp
x655-859 y189-209 (w 204 h 20 = diagonal), not the original's horizontal pair.
Render TR also shows a central blue depression (blue px 1,947 vs orig 781) and
double the peak color. Not refuted.

## MINORs
#6 TL re-plot scaling — advisory, surface type preserved. #7 "Non- Convex" hyphen
spacing — whitespace-only, low confidence, not acted on.

## Disposition
4 of 5 MAJORs stand (only #3 refuted) -> slide 025 NOT certified. No DB write
(gen_status stays 'building', visual_check stays empty, last_error untouched), no
final_deck_tool update, no render_check_pages run. result.txt rewritten (old ->
result_att_stale.bak). Crop fresh leg still in flight at write time; its verdict
and `rejudge_adjudicate.py 025 --crop` output banked alongside. No git; no
evidence deleted.
