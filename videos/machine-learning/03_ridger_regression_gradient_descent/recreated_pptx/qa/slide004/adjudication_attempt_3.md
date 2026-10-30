# Adjudication of judge_attempt_3.txt (Template A on render_3 — FAIL)

Verdict: **FAIL**, driven solely by finding #1 (vector subscript `n` vs `N`).
The judge says of its own MINORs: *"The two MINORs alone would not fail the slide."*
All findings adjudicated PIL-first on the ORIGINAL frame
`unique_slides/slide_004.jpg` (960×540, 1 frame px = 1 pt) before any build change.

---

## Finding 1 — vector subscript `n×1` vs `N×1` (MAJOR / high)
**VERDICT: REFUTED — the original is lowercase `n`. No build change.**

This is the third consecutive verdict in which this judge claims the original uses a
capital `N`; the claim is uncorroborated and was already refuted in
`adjudication_attempt_2.md`. Re-verified under the same t=205/215/225/235/245 sweep
described there. The measured glyph (both boxes: x188..209 and x533..554, identical
inter-glyph gaps ≈5 then ≈4 px) is two parallel legs joined by an arch at the TOP:

```
t=225   y198 ..#######..     <- arch fills the top ACROSS the full width
        y202 ..##..##...     <- legs stay separate to the bottom
```

A capital `N` is defined by a diagonal from top-left to bottom-right and would show
ink in the inter-leg gap at some threshold — it never appears. Independent
corroboration: `analysis/slide_004_final.json` verbatim_text and equations record
`n \times 1` for both column vectors.

The judge's internal-consistency argument is also backwards: it argues the recreation
is self-inconsistent for writing `n` in the vectors while writing `N` for X and Y in
the Where block — but that is exactly the original's own convention (subscript on the
column vector = `n`, sample-count in the feature matrix = `N`), i.e. the recreation is
faithful to the source, not inconsistent.

**Decision: no change. Mathtext stays `\right)_{n \times 1}`.**

---

## Finding 2 — "Where:" line spacing (MINOR / medium)
**VERDICT: PARTLY CONFIRMED — two real gaps; both fixed.**

Measured original Where-box bands (x500..870): **285..303, 314..337, 345..363** →
tops 285/314/345, pitch 29 then 31.
Measured render_3 bands: 283..292, 308..320, 335..344, 361..369 → pitch ~26.

The judge's *direction* is wrong (mine were **tighter**, not "more widely separated"),
but two genuine structural gaps were measured:

1. **"Where:" is INLINE with the X fact in the original** — full-res read of
   x500..600 y285..303 gives W(h)ere: as glyphs 1..6 (x507..569) and the X glyph
   from x573 onward, all on one line. The build had "Where:" alone on its own line.
2. **Fact-line pitch is ~30 px**, not 26.

**Fix applied:** `WHERE_LINES` merged into 3 entries with "Where: " (bold)inlined
into the first; `WHERE_Y = 285`, `WHERE_PITCH = 30`. Verified on render_4:
bands **285..297, 315..327, 345..357** (pitch 30/30), matching the original.

---

## Finding 3 — left-column box borders navy vs black (MINOR / medium)
**VERDICT: REFUTED — the original's borders are dark navy, not black.**

Darkest-pixel sampling of each border row in the original:

| Box | Border row | dark px |
|---|---|---|
| Objective | y244 x110..270 | **(37, 31, 117)** |
| Error | y308 x110..450 | (34, 30, 115) |
| Formula | y465 x110..450 | (26, 17, 110) |
| Define | y390 x110..620 | (145, 22, 27) = red |

The Objective/Error/Formula borders are blue-violet (r,g < 40, b > 110) — consistent
with the build's `NAVY = "000080"`. Define is red, matching the build's `RED`.
**No change.**

---

## Finding 4 — left-stack box proportions (MINOR / medium)
**VERDICT: REFUTED.**

Measured original box right edges vs render_4 build values: Error x486 = original
x486 (exact), Formula x486 = exact, Define build x660 vs original x654 (0.9%). All
within measurement tolerance; the judge's "right edge ~53%" reading is not reproduced.

---

## Finding 5 — "from Model Ŷ=XW" spacing (MINOR / medium)
**VERDICT: REFUTED per ground rule (d).** Spacing inside a handwritten phrase vs a
typeset one is the inherent typed-vs-handwritten medium difference; the verbatim text
matches the founder record (`from Model Ŷ=XW`).

---

## Finding 6 — "Objective is Ŷ=Y" underline (MINOR / low-medium)
**VERDICT: CONFIRMED — fixed.**

Full-res read of the Objective box (x80..305, y242..301) shows a 17 px bar at
**x254..270, y283..284**, sitting directly below the italic `Y` glyph (which ends at
y282) — an underline, and the only one on the slide (an identical scan of the Error
box found no comparable bar).

**Fix applied:** a 1 pt `INK` line at frame x254 w17, y283. Verified on render_4:
underline renders at **x254..271, y282..283**, matching the original to ±1 px.

---

## Finding 7 — Remember box vertical placement (MINOR / low)
**VERDICT: REFUTED.** Original Predicted-Labels box spans y100..221; the original
Remember fill spans y100..152 — i.e. **top-aligned** with the Predicted box, not
centred against it. The build places it at y100..153, the same convention.

---

## Summary of the render_4 build changes

| file | change |
|---|---|
| `recreated_pptx/build/slide_004.js` | "Where: " inlined into the first fact line; `WHERE_Y` 282 → 285; `WHERE_PITCH` 26 → 30 |
| `recreated_pptx/build/slide_004.js` | added 1 pt `INK` underline at x254 w17 y283 (Objective box) |

Equation assets, the vector subscript case, the box geometry and the single Remember
box are unchanged.

## Verification of render_4 (all green)

- `house_chrome_check.py render_4.png 4` → **PASS** (strokes L/R/bottom present, top
  bare, badge centre (1824,152) d=68, tol 8).
- `pdftotext` → every verbatim line present; the Where block now reads
  `Where: X_{N×(d+1)} is a matrix ⇒ Given` / `Y_{N×1} is labels vector ⇒ Given` /
  `W is Model Parameter ⇒ Required` (⇒, three separate pinned lines).
- Where line pitch 30/30 and underline x254..271 y282..283 measured on the render.
