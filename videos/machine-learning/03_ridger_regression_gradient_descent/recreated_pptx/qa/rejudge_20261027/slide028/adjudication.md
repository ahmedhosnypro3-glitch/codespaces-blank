# Adjudication — slide 028 FULL FAIL (rejudge_20261027, full leg)

Adjudicated 2026-10-30, read-only except these notes. No build script, pptx, or DB touched.

## Claim under adjudication

Transcript: `judge_full_retry.txt` (the retry is the banked FAIL; `judge_full.log` is empty).
Images: `render.png` (2001×1125, scale 2.0844/2.0833) vs `unique_slides/slide_028.jpg` (960×540, 1 px = 1 pt slide space).

Findings listed in the transcript:

| # | severity | claim |
|---|---|---|
| 1 | MAJOR | Plot-region proportions/alignment: original's right (large-LR) region is the wider one and the pair asymmetric/tighter (the two "Value of weight" termini sit close together near slide center); recreation made the regions ~equal width, pushing the labels apart / larger central gap (confidence medium-high) |
| 2 | MINOR | Small-LR descent floor: lower staircase steps sit marginally closer to the x-axis/bottom border in the recreation (confidence medium, "cosmetic only") |

FINAL VERDICT in transcript: FAIL, "driven solely by the MAJOR plot-proportion/alignment deviation (item 1)". All element rows (title, badge, subplot titles, axis labels, both charts' content, blue frame, containment) were MATCH.

## Pixel evidence (PIL, slide-space px; red mask r>100, r−g>50, r−b>50; teal g>140, b>150, b−r>30, g−r>25; dark ink sum<450; blue frame b>80, b−r>30, b−g>20, r<130)

`rejudge_adjudicate.py 028 --full`: 118,415 diff px (5.260% of frame); ink only in render 14,810 px, only in orig 62,994 px (expected: orig JPEG AA on all text/curves). Densest diff cells are ALL in text/badge bands — badge x864-888 y67-90 (1015), title x192-312 y67-90 (905-964), "Value of weight" labels x264-456 / x600-792 y427-472, headings x264-288 / x600-624 y180-202. No dense diff cell inside either plot interior → no layout shift, only glyph AA.

Geometry, ORIG vs RENDER (slide-space px):

| quantity | ORIG | RENDER | delta |
|---|---|---|---|
| blue enclosing frame | x 90..858, y 127..509 | x 89.2..856.9, y ~127..507.8 | <=1.1 |
| left x-axis (shaft+arrow) | x 158..427, y 442..443 | x 159.8..427, y 440.6..441.6 | <=1.4 |
| right x-axis | x 512..779, y 435..443 | x 508.5..779.1, y 437.8 | <=3.5 |
| left y-axis | x 158, head y 212, shaft to y 433 | x 157.4, head y 208.3 | <=0.6 |
| right y-axis | x 511, head y 208, shaft to y 431 | x 509.5, head y 205 | <=1.5 |
| LEFT plot width (y-axis -> x tip) | 427-158 = **269** | 427-157.4 = **269.6** | 0.6 |
| RIGHT plot width | 779-511 = **268** | 779.1-509.5 = **269.6** | 1.6 |
| left:right width ratio | **1.004 (right 1 px NARROWER)** | **1.000** | — |
| central gap (left x-tip -> right y-axis) | 511-427 = **84** | 509.5-427 = **82.5** | 1.5 |
| "Value of weight" left label ink | x 366..454 | x 367.5..453.9 | <=1.5 |
| "Value of weight" right label ink | x 711..799 | x 711.5..797.8 | <=1.2 |
| subplot heading clusters (centers) | x 240..373 / 589..721 (c 306.5 / 655) | x 238.9..371.8 / 587.7..721.1 (c 305.4 / 654.4) | <=1.1 |
| title red ink bbox | x 191..690, y 72..101 | x 186.6..690.9, y 73.4..100.8 | <=4.4 (AA edge) |
| teal left curve bbox | x 161..383, y 235..440 | x 160.7..382.8, y 235.2..444 | <=1.5 |
| teal right curve bbox | x 514..737, y 231..437 | x 513.8..735.5, y 232.8..436.3 | <=1.5 |
| right rise tip -> frame right clearance | 858-737 = 121 | 856.9-735.5 = 121.4 | 0.4 |
| left plot floor gap above x-axis top | 442-440 = **2.0** | 440.6-439.7 = **0.9** | ~1.0 |
| right plot floor gap above x-axis top | 439-437 = **2.0** | 436.8-435.8 = **1.0** | 1.0 |

House chrome: `chrome_check.txt` = PASS (panel, L/R/bottom strokes, no top stroke, badge at (876,73)) — matches the transcript's own "settled chrome" row.

## Vision re-read leg

Optional one gate leg SKIPPED: `pgrep -c -f analyze_image.py` = 26 (>= 8) while the rejudge wave drivers occupy the shared gateway; PIL adjudication is the register's primary evidence and is decisive here.

## Dispositions

- **Claim 1 (MAJOR, plot proportions/alignment): REFUTED.** In the ORIGINAL itself the two inner plot regions are equal width — left 269 px vs right 268 px (the right is 1 px narrower, not wider) — with central gap 84 px and "Value of weight" labels at x 366..454 / 711..799. The recreation matches every one of these quantities within <=1.5 slide px (<=3 render px). There is no original-side asymmetry or tight center gap to reproduce; the claimed "wider right region / termini close together near center" does not exist in the bytes (likely a misread of the capture cursor near the left plot floor or center JPEG noise — the transcript itself notes the cursor artifact). DISMISSED per register rule (vision claim refuted by pixels).
- **Claim 2 (MINOR, small-LR floor clearance): CONFIRMED in direction, negligible in magnitude** — 1.0 slide px (2 render px) closer to the axis than the original, matching the transcript's own "cosmetic only"; below AA/JPEG noise, both floors sit 1-2 px above the axis in both images. Not a MAJOR, not a fix trigger.
- All transcript MATCH rows corroborated by geometry (title, headings, labels, frame, containment with 121 px right clearance, both charts' ink extents).

Net: the slide 028 FULL FAIL is **overturned**; the certification stands. No fix dispatched.
