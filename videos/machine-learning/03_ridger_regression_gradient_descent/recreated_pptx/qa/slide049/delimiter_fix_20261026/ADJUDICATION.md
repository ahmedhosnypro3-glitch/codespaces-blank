# Slide 049 — straight-delimiter fix (founder directive 2026-10-26, PIL-only)

## Directive (verbatim, founder in-session)

> "slide 49 has same paranthes defect, fix it intelli[g]ently"
> "on slide 49, these are matrcies multiplication, and now, the iteration block
> equation's left matrices don't have parenthes, and they should be straigh lines,
> not curved, which is much easier, i mean [1 1 1].[5 -1 1] = 3 but u made them
> curved, and "1 1 1" don't have parentheses"
> "slide 49 paranthese must follow slide 45 (certified working)"
> "no fucking curve on the parantheses at all"

Resolution: every paren asset (top2 / Z / aug / initial-W / wcol dx+W) replaced by
straight 1px-rect bars at measured bulge centers; the bare triplets get straight paren
pairs ADDED (they had none); all re-laid digits placed at measured centroids; 45's
certified bar idiom and colors followed.

## Changes to build/slide_049.js (single deliverable slide_049_recreated.pptx, rebuilt)

- New `dbar()` helper; `path`/`fs` requires, `ASSET_DIR`, `sidecar()` and every
  addImage paren call removed (grep-clean: no sidecar/ASSET_DIR/addImage left).
- New consts: PGRAY A6A6A6 (triplet+dx bars), IGRAY 6E6E6E (initial-W bars),
  DGREEN 008000 (dx digits).
- top2: 12 bars y77 h31 909090, L [89.81,111.95,133.86,156.28,179.34,202.25],
  R [101.37,123.59,146.15,169.01,191.46,213.61].
- Z grid: 6 bars y86 h33 909090, L [640.96,664.10,686.30], R [654.65,676.56,699.07].
- Aug: 12 bars y180 h46 909090, L [93.59,115.28,137.43,160.65,182.66,205.64],
  R [105.84,127.15,149.74,172.35,195.05,217.20].
- initialW: 2 bars x330.28/351.72 y57 h49 6E6E6E + digits [4;−2;−2] at '4'@341.5,
  '−2'@344.5, cys 66.5/82.5/97.5, 13pt Arial BLACK.
- Calc rows (B = 140/206/272/338/404/470): triplet paren bars `(` x329.0 y=b+7 h13,
  `)` x375.0 y=b+8 h12, PGRAY (ADDED — triplets previously bare); dx bars x378.5/401.0
  at measured per-row spans DY=[[145,192],[214,260],[277,324],[347,392],[410,456],
  [475,522]], PGRAY; dx digits [5;−1;−1] '5'@392, '−1'@393.5 (U+2212), cys b+12/b+29/
  b+45.5, 12pt Arial DGREEN; W bars x722.3/744.0 (r1-3) and x733.8/755.4 (r4-6), same
  spans, DGRAY 909090; W digits '5'@733.5/'−1'@736 (r1-3), '5'@745.5/'−1'@748 (r4-6),
  same cys, 12pt Arial BLACK.
- Untouched: certified triplet digit cells (centres 335/353/371, RED rows1-3 / INK
  rows4-6), d(x) labels, =, results 3/2/2/−4/−6/−7, ⇒, verdicts, "W =", rules, panel,
  legend, tables, chrome. Arithmetic re-verified: (row)·[5;−1;−1] = 3/2/2/−4/−6/−7.

## Verification (all PIL, deterministic; verify_bars.py in this dir)

- 125/125 PASS: 68 bar longest-run centers within tolerance; 18 GREEN dx + 18 BLACK W
  + 3 BLACK iw digit centroids within 5 render px; 18 untouched triplet digits
  (RED/INK masks) present at certified positions; diff vs a fresh render of the banked
  HEAD build (the edit base) >8: 36,413 px, ALL inside the paren/digit edit zones +
  chrome hairline jitter bands — 0 strays. (An earlier zone-diff against the banked
  SWEEP-variant render showed 6,580 strays — that baseline carries the superseded
  sweep lane's own non-paren changes and is NOT the edit base; kept only as evidence.)
- house_chrome_check.py: PASS.

## Bytes

| file | md5 |
|---|---|
| before_render_head_150dpi.png (edit base = HEAD 1f456b09) | 9ba0b8a982e0c899df7a6b3e9b7a346f |
| before_render_sweep_150dpi.png (superseded sweep variant) | 12177f2eee09b775bd4a632bc188e3cc |
| after_render_150dpi.png | 3b2d36a6183245aff673dbcaebbc3e50 |
| slide_049_recreated.pptx (new, committed) | 812b17c017804c0bdabdaa14dc7ae085 |
| HEAD js copy (slide_049_HEAD.js) | see md5s_before.txt |

## Flagged observations

- dx column digits were black in the superseded sweep variant (via PNG); the original
  frame's digit cores are pale green (132-146,168-174,131-149) → re-laid as DGREEN
  008000 text, a fidelity fix landed with this directive.
- The superseded sweep variant (curved delimiters) is banked under
  qa/paren_sweep_20261026/superseded_pptx/ with its md5s; the four files it had
  modified (slide_049.js, eq_slide049_wcol_paren.json, render_wcol_049p.py,
  slide_049_recreated.pptx) were restored to HEAD before editing.
- Sibling lanes 043/050/051 were in flight during this fix; their files were never
  touched. Deck page 49 replaced; merge gate PASSED (0 px differ).

## REDO ADDENDUM (2026-10-26 15:2x, same founder directive)

Two concurrent fleet restores destroyed the fix AFTER it was built and verified: the
14:44:36 `git checkout` reverted slide_049.js + slide_049_recreated.pptx to HEAD
(1f456b09's Bezier top2 build) — the deck page embedded at 14:22 (812b17c0 bytes)
survived only inside the deck package. The fix was re-applied to the js from THIS
spec (dbar; top2/Z/aug/iw/triplet/dx/W bars; DGREEN dx digits; BLACK W + iw digits),
rebuilt, and re-verified: verify_bars.py EXIT PASS 0 failures (125/125), zone diff vs
the banked HEAD baseline 36,412 px with 0 strays (matches the 36,413 recorded below),
diff vs the banked after_render 161 px 0 strays, chrome PASS,
sidecar/ASSET_DIR/addImage grep-clean. Corrected bytes:

| file | md5 |
|---|---|
| slide_049_recreated.pptx (redo build, committed fd6530a6) | 5917ea7de132b26692eda26a76a6fcfb |

Deck page 49 re-replaced (deck md5 f4c84e38734e9bd82b88ba1d159a5745); merge gate PASS
(0 px differ, gate_20261026-152116_p45-47-49).
