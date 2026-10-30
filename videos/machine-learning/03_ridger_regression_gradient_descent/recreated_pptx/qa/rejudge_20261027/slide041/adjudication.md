# Slide 041 — rejudge FULL FAIL adjudication (2026-10-30, read-only)

Transcript adjudicated: `judge_full_retry.txt` (retry leg of the FULL comparison;
`judge_full.log` first attempt produced no transcript). Images: `render.png`
(2001x1125, 150 dpi) vs `unique_slides/slide_041.jpg` (960x540), slide-space scale
2.0844 (task-stated 2.0833). Helpers: `../rejudge_adjudicate.py --full`,
`adjudicate_pil.py`, `adjudicate_pil2.py` (this dir; read-only, slide-space px).

Vision re-read leg: NOT run — optional per tasking; gate busy
(`pgrep -c -f analyze_image.py` = 30 at start, 25 after 45 s; gate requires < 8).

## Findings in the transcript and their dispositions

### 1. MAJOR — "input-vector table has an extra column; recreation invented x3=(1;2)/C1; original shows 5 columns x1,x2,x4,x6 with a gap, class row C1 C1 C2 C2 C2" — REFUTED

PIL measurements on the ORIGINAL frame (slide space):

- Header row y58-73, neutral-ink runs x60-240: SIX groups at
  x92-100, x114-123, x136-145, x158-168, x181-191, x204-213.
  Inter-group gaps uniform 13-14 px — there is NO gap at column 3; the x136-145
  group is present with the same pitch as all others. Render headers: six clusters
  x93-99, x115-121, x136-143, x159-166, x182-188, x205-211 — same positions.
  Per-header orig-vs-render crop diff is uniform (~49-51 px > 90 for all six).
- Vector band y76-112: SIX (left-paren, digit, right-paren) triplets. Column 3
  (x134-147) has its paren pair at x134/x147 and digit ink at x138-142 (27 px);
  its band is 53% cream vs 44-52% for the other five columns — inked like the
  rest, not blank.
- Class row y108-124: red ink at x90-92 (col1), x114-115 (col2), x135-137 (col3)
  = THREE red C1 labels; blue at x158-159 (col4), x180-181 (col5); col6 x200-216
  carries the C glyph (dark 31 px) + blue subscript (blue 7 px loose). Render:
  red clusters x92-100, x113-121, x135-143; blue x158-166, x181-189, x203-211.
  Both images read C1 C1 C1 C2 C2 C2 — the judge's "only two red C1" is wrong.
- Per-column diff (threshold >90) in the table region y54-130 is uniform:
  cols 1-6 = 414/437/439/452/448/444 px; digit bands only = 100/122/111/121/112/121
  (top) and 106/117/129/118/125/120 (bottom). No spike at column 3 — the render's
  col3 matches the original as well as every other column matches.
- Corroboration: `build/slide_041.js` header records that the analysis JSON's
  "x1 x2 x4 x5 x6" 5-column reading was a self-flagged vision misread
  (`analysis/slide_041_final.json` uncertain_items) and was PIL glyph-verified at
  build time as SIX columns (1,1)(2,1)(1,2)(5,4)(6,5)(6,6), classes C1 C1 C1 C2 C2 C2.

### 2. MINOR — "W column vector drawn with '(' in recreation vs '[' in original" — REFUTED as a discrepancy

Bow profile of the W delimiters (neutral ink, y57-107, x327-336 / x349-358):

- ORIG left delim: leftmost ink top-third x331, mid x330, bottom-third x330-335 —
  the middle bows LEFT of the top => curved "(" (a "[" would keep a constant
  leftmost x with wide horizontal serifs at top AND bottom).
- ORIG right delim: mid spans x349-353 (w=5) vs top x352-353 (w=2) — middle bulges
  left => curved ")". Render shows the same bow signature (left mid x328 vs top
  x329; right mid x352-353 vs top x350-351).
- The original is handwritten ink; the transcript itself rated this style-only at
  ~60% confidence ("likely inherent to the typed-vs-ink conversion"). Not a
  content discrepancy; at most the known medium-difference note already covered by
  the judge ground rules.

### 3. Transcript's non-findings — confirmed settled (no action)

House chrome per deck-03 template (no top stroke is correct; badge "41"
yellow/purple correct), mouse-cursor omission correct, scatter plot/axes/markers
exact, all top-box text verbatim ("Initial W =", "Step η = 2", "Check classes of",
Z1 Z1 Z1 with (0;0)(7;6)(3;2), W=(4;-2;-2)).

### 4. Full-frame context

`rejudge_adjudicate.py 041 --full`: 117,586 diff px (5.223%) at threshold >90;
densest cells all in the legend row y112-135 (text anti-aliasing); no
column-shaped diff mass in the table. Ink only in original 60,090 px vs only in
render 17,096 px — handwritten ink is heavier than typed text, not missing content.

## Disposition

FAIL DISMISSED. The verdict rested solely on the MAJOR claim, which the pixels
refute on every axis (header count, gap test, paren/digit presence, class-label
colors, per-column diff uniformity). Per the register rule, a vision claim refuted
by pixels is DISMISSED. Slide 041's certification stands; no reopen, no rebuild,
no edits to builds/pptx/DB.
