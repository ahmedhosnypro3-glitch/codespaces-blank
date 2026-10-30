# Slide 047 — straight-delimiter fix (founder directive 2026-10-26, PIL-only)

## Directive (verbatim, founder in-session)

> "slide 47 dz functions parentheses are curved, just make them straight"
> "no fucking curve on the parantheses at all, that it is why slide 45 is good at that"

Resolution: every curved delimiter on the slide — the five paren PNG assets
(paren_p047_tl2 / _z / _aug3 / _w / _stack) AND the calc row-vectors' curved font
parens "(1 0 0)" — replaced by straight 1px-rect bars at measured bulge centers;
row-vector digits re-laid to measured centroids between the bars.

## Changes to build/slide_047.js (single deliverable slide_047_recreated.pptx, rebuilt)

- New `dbar(x,y,h,color)` helper (the certified 1px-rect idiom); `img()` helper,
  `ASSET` const and all PAR_X/PAR_W consts removed (grep-clean).
- tl2 matrix: 12 bars y77 h31, color 909090, L x [89.81,111.45,133.54,156.30,178.75,201.69],
  R x [100.50,122.84,145.10,168.06,189.78,212.36].
- Z matrix: 6 bars y86→80 h32, 909090, L [598.06,621.45,643.03], R [609.92,632.78,654.45].
- Aug matrix: 12 bars y180 h46, 909090, L [93.27,114.66,137.11,159.49,182.17,204.63],
  R [105.67,126.09,149.00,171.29,193.88,215.93].
- Initial-W vector: 2 bars x330.5/352.0 y57 h50, 6E6E6E (digits unchanged at cx340).
- Calc rows (dy 0/69/135): triplet `(` x330.0 y147+dy h13, `)` x378.0 y148+dy h12,
  A6A6A6; row-vector digits now three cells at cx 336/353.5/369.5, cy 153.5+dy,
  13pt Times BLUE 1A1A99 (content from b.row, parens stripped); stack column bars
  x380.9/403.95 y145+dy h48 (h47 for dy135), A6A6A6, digits moved cx 397→395.
- Untouched: d(Z) labels, results, sign statements, class outcomes, tables, chrome.

## Verification (all PIL, deterministic; verify_bars.py in this dir)

- 62/62 PASS: 44 bar longest-run centers within tolerance (max dev ~1 render px);
  9 blue row-vector digit centroids + 9 green stack digit centroids within 5 render px;
  diff vs pre-edit render >8: 18,892 px, ALL inside paren/digit zones (after widening
  two zones by 1.5 frame px to absorb the OLD paren PNGs' edge antialiasing — expected
  removals) + chrome hairline jitter bands. 0 strays.
- house_chrome_check.py: PASS.

## Bytes

| file | md5 |
|---|---|
| before_render_150dpi.png (certified pre-edit) | e84972f1d2b9d35cf38ccdcec8923133 |
| after_render_150dpi.png | 2c36b3c636595fff5a8cd64388fc5139 |
| slide_047_recreated.pptx (new, committed) | 7a6a73103f61839a082501cf6a0c928c |

## Flagged observations

- The Z-matrix bars sit at y80 h32 (probe-locked) though the old PNG box started at
  y79 — probe measurement wins.
- Stack digits cx 397→395 follows the measured bar-span center; certified digit
  colors (GREEN 008000, 10.5pt Times) unchanged.
- Deck page 47 replaced; merge gate PASSED (0 px differ).

## REDO ADDENDUM (2026-10-26 15:1x, same founder directive)

A concurrent fleet lane's `git checkout` (14:10:43) reverted both slide_047.js and
slide_047_recreated.pptx to HEAD (pre-fix) AFTER the fix was built and verified; the
deck update at 14:22 therefore re-embedded the OLD page. The fix was re-applied to the
js from THIS spec (dbar helper; tl2/z/aug/W/stack bars; row-vector digits cx
336/353.5/369.5; stack digits cx 395), rebuilt, and re-verified: verify_bars.py
EXIT PASS 0 failures (62/62), diff signature identical to the record below
(18,892 px, 0 strays), chrome PASS, img()/ASSET/PAR_ grep-clean. Corrected bytes:

| file | md5 |
|---|---|
| slide_047_recreated.pptx (redo build, committed 3a2668b0) | fcfd2713e095d8ad9e26459ac0035776 |

Deck page 47 re-replaced (deck md5 f4c84e38734e9bd82b88ba1d159a5745); merge gate PASS
(0 px differ, gate_20261026-152116_p45-47-49).
