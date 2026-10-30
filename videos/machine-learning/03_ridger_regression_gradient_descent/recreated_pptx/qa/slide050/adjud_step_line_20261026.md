# Adjudication — cross-slide underline law, 049 + 050 Step-line & Initial-W label (2026-10-26)

## The corrected story (pixel-proven, 1px + multi-threshold forensics)

`unique_slides/slide_049.jpg` and `unique_slides/slide_050.jpg` are
**pixel-identical** across the whole Initial-W / Step-line zone
(top-box ink XOR = 84 scattered JPEG px over x68..739 y59..129; label-zone
XOR = 3 px; dark Step-band IoU = 1.000 at identical rows). Both originals
show, on ONE line above the Initial-W row:

1. dark glyphs "Step η = 1" — x366..421, y59..71 (identical bitmaps both slides)
2. a **real underline bar** y71..72, x366..419 — 2px, JPEG-faded gray-dark
   (57/60 px < lum 180 on each row; NOT continuous at <140, gaps at x390..393
   and x407 are fade, not absence)
3. red "REPEAT using Step" — x425..530, y60..74 (red bbox identical both
   slides; ink mean RGB (215,121,120) both)

The Initial-W label itself ("Initial W =", x267..321 y75..84, vector column
x330..353 with parens ink y62..102) has **NO underline under its W** on either
original (x294..325 y83..96 blank to <200; same on slide_042).

## How three wrong readings happened (so they do not recur)

- **read_initialw misattribution (slide 042 cert era):** the real Step-line
  underline band (x364..423, y71..73 at JPEG blur) was attributed to the
  label's W. 042's build comment "the frame's W is bold-italic-underlined"
  is false per pixels; the pattern propagated into 050's build (14pt label,
  W bold-italic-underlined) and an old 049 build note ("underline band
  y72..73 x364..423").
- **"NO underline anywhere" (049 label fix, earlier this window):** the
  correction over-shot — it removed the build's standalone underline band,
  which was the REAL Step-line underline, and the att17 work then found the
  049 build had ALSO lost the dark "Step η = 1" text entirely (it drew one
  all-red "REPEAT using Step η = 1" at x426, ~30px too wide, with "η = 1" in
  the wrong color at the wrong end).
- **att15 judge misattributions (DESC-primed):** the att15 top_band judge
  claimed "in the original the underline is beneath W" — it saw the real
  Step-underline band in the crop and attached it to the label line below;
  and it called the all-red REPEAT line "faithful" because the DESC told it
  the line reads "REPEAT using Step eta = 1". Both dismissed per pixels.

## Fixes applied (attempt 17, both slides)

- **050** `build/slide_050.js`: removed `underline: true` from the label's W
  run (bold italic kept). render_16 → render_17 diff = exactly x299..312
  y87..88 (the 2-row phantom bar, 112 px) and nothing else.
- **049** `build/slide_049.js`: replaced the single red text with 050's
  certified composition — dark italic underlined "Step η = 1" at x365
  (12.5pt, y56 box) + red bold "REPEAT using Step" at x425 (11pt, "92211B" =
  050's CHART_RED; origs identical so the reds must match). render_16 →
  render_17 diff = exactly the Step-line band x365..567 y60..74.
- House chrome PASS both; render_17 PIL geometry matches origs (Step-ink
  x365..422 y60.8..72.3 vs orig x364..423 y56..72; underline y71.5..72.0
  x366..421.7 continuous vs orig y71..72 x366..421; red x425.9..527.7 vs
  orig x425..530). Label-zone deltas are glyph-descender ink (max row n=13/16
  vs orig 7 at <200) — typography-minor, no bar.

## Standing law for this deck (underline class)

- The x366..421 y71..72 band under "Step η = 1" is REAL on every
  Initial-W/REPEAT slide whose orig shows the band — verify per slide, never
  copy 042's "underlined W" pattern.
- A label W-underline is a PHANTOM unless that slide's own orig shows a bar
  under the W glyphs specifically (049/050/042: it does not).
- Judge claims about underline placement are adjudicated at 1px against the
  orig before any fix; DESC wording must never assert underline state that
  pixels have not confirmed.

## Carry state after att17

- 049: aug_box + iter_stop (0-diff from att14) + calc_rows (att15 PASS)
  carry — att17 diff zone (x365..567 y60..74) is outside their crop regions.
  Re-judge att17: top_band, legend (pending 132px-intrusion finding), legA.
- 050: pinkbox + redstop (0-diff) carry. Re-judge att17: mathzone, tableeq,
  chart, caption, legA.
- 051 note: label zone XOR vs 050 = 7 px (same label, no W-underline) but the
  Step-line differs (red bbox x420..435 y67..77 — short red "Step η = 1",
  build comment agrees); 051's own HANDOFF governs its rewrite.

## Addendum 2026-10-26 (att18) — word-order correction

The att17 reading above — dark underlined "Step η = 1" + red "REPEAT using
Step" — has the two texts SWAPPED (same zone; origs pixel-identical with
049, dark-band IoU 1.000). att18 truth: black italic underlined "REPEAT"
x366..421 y61..70 (six caps-height glyphs, zero descenders; underline
y71..72 x366..419 real) + red "using Step η = 1" x425..530 y60..74 (i-dot
x442; descenders g/p/η at x452/481/508). 050's build was rewritten the same
window: "REPEAT" black italic underlined (box x365 y56 w64 h18) + "using
Step η = 1" red bold italic (92211B kept; the att17 C2-color judge finding
was a misread — render C2 blue x312..324 ≈ orig x312..326); the phantom
label W-underline was already removed at att17. render_18 PIL-verified; the
r17→r18 diff is confined to x365..531 y60..74. The standing-law bullets
above keep their pixel locations but sit under "REPEAT", not under
"Step η = 1".
