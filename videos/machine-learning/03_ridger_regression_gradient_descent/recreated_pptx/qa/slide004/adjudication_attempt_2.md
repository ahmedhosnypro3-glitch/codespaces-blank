# Adjudication of slide 004 judge_attempt_2.txt (Template A, FAIL)

All findings adjudicated with PIL on the ORIGINAL frame `unique_slides/slide_004.jpg`
(960x540, 1 frame px = 1 pt) BEFORE any build change, per the judging law.
`ink` below = pixel with (r+g+b)/3 < threshold.

---

## Finding 1 — "Missing labeled callout Remember for the W fact" (BLOCKER / medium-high)
**VERDICT: REFUTED — no build change.**

The judge claims a second "Remember" callout wraps "W is Model Parameter → Required"
in the lower-right Where block, and that the Where block is "flattened".

Measured original structure (red-border runs, `str` = stroke thickness):

```
red verticals   x80   x494   x883        (x683/744 = title text, not borders)
red horizontals y100  x427..744, x784..878     <- Original Labels / Predicted Labels / Remember box tops
                y220..222  x80..395, x425..745  <- box bottoms
                y232..234  x493..883            <- Where box TOP border
                y370..371  x493..883            <- Where box BOTTOM border
```

There is exactly ONE "Remember" box in the whole frame: **x784..880, y100..152**
(top-right), with an internal divider at **y118, x795..869** (len 75) separating the
"Remember" caption line from the `‖a‖₂ = aᵀa` identity below it. It is 95 px wide.
The Where box spans x493..883, y232..371 — 390 px wide, and its five text lines sit
inside it as plain lines beginning "Where:". No second callout, no "Remember" prefix
on the W line, and no fill or border distinguishes the W fact.

Corroboration already on file: `qa/slide004/judge_attempt_2.txt`'s own "Confirmed
correct" list agrees the bottom equation renders, and the build header comment
(slide_004.js lines 10-13) records the same single-Remember-box geometry from an
independent PIL pass.

**Decision: do NOT add a second Remember callout.** The judge invented the element.

---

## Finding 2 — vector-subscript case `N×1` vs `n×1` (MINOR / medium)
**VERDICT: REFUTED — the original is lowercase `n`. No build change.**

Two matching 3-glyph subscript clusters exist, one under each column vector:

```
LEFT  (Y vector)   glyphs at x188..193, x198..203, x207..209   rows 196..203
RIGHT (Ŷ vector)   glyphs at x533..539, x544..548, x552..554   rows 201..208
```

Inter-glyph gaps are identical in both (≈5 px then ≈4 px), so both subscripts are
the same string. Glyph 3 is a bare 3 px-wide vertical stem = `1`. Glyph 2 has a
diagonal cross (two strokes crossing) = `×`. Glyph 1, read at t=205/215/225/235/245:

```
t=205   y196 ...###.##..     y201 ..##..##...
        y198 ...###.....     y203 ..##.......
t=225   y198 ..#######..     y202 ..##..##...     <- arch joins the legs at the TOP
```

Shape: two parallel legs joined by an arch at the top, **no interior diagonal at any
threshold**. A capital `N` is defined by a diagonal from top-left to bottom-right,
which would show as ink in the gap (e.g. `#.##`, `#..#`) at some threshold — it never
appears; instead the top rows fill solid. Height 8 px, leg gap ~3 px → lowercase `n`.

Independent corroboration: `analysis/slide_004_final.json` verbatim_text and
equations record `n \times 1` for both column vectors, and the AGENTS.md deck note
verbatim lines carry `(y₁, y₂, ..., yₙ)_{n×1}`. Both the frame and the
founder-validated record agree.

**Decision: keep lowercase `n \times 1` in eq_004_Yvec / eq_004_Yhatvec. No re-render.**

---

## Finding 3 — arrow glyph in the "Where:" facts, `→` vs `⇒` (MINOR / high)
**VERDICT: CONFIRMED — the original uses `⇒`. Build changed.**

Long-horizontal-ink-run scan over the whole body found the arrow bars:

```
line 2 ("...is a matrix ⇒ Given")   y290 x772..784 len13 ; y291 x772..785 len14
                                     y294 x772..785 len14 ; y295 x772..784 len13
line 3 ("...labels vector ⇒ Given") y323 x775..786 len12 ; y324 x775..787 len13
                                     y327 x775..786 len12
```

The same four-bar handwriting recurs. Reading the glyph at x771..785, y286..299
full-res:

```
 289 ....###..........          <- arrowhead apex
 290 #############...          <- upper shaft (len 13)
 294 #############...          <- LOWER shaft (len 13)
 296 ........###....           <- lower-shaft right end
 298 ..........###...          <- lower-shaft tip
```

**Two stacked horizontal shafts ~4 px apart** = a double-shaft `⇒` (RHS arrow), NOT
the single-shaft `→`. This is the same glyph the judge itself praised as matching in
`If Ŷ≠Y ⇒ There is an Error (Loss)` — measured there too, at x211..231
(y329..331 and y335..336, len 20) and preceded by the `≠` at x329..348 (no ink in the
crossing row 335) — i.e. the Error box's `⇒` was already correct in the build.

**Fix applied** to `recreated_pptx/build/slide_004.js` lines 197-199: the three
`→` in the Where facts changed to `⇒`. The `_{...}` subscript braces are ASCII
(`X_{N×(d+1)}`, `Y_{N×1}`) because GROUND RULES clause (e) mandates professional 2D
formatting and the braces denote the professional subscript grouping — unchanged.

---

## Finding 4 — `X_{N×(d+1)}` vs `X_{N×d+1}` (MINOR / low, informational)
**VERDICT: REFUTED as a defect — keep the parens (no change).**

The parens are in the founder-validated spec (`analysis/slide_004_final.json`
verbatim_text: `Where: X_{N×(d+1)} is a matrix → Given`) and the judge itself calls
it "a professional-formatting choice, not a data error". GROUND RULES clause (e)
mandates professional 2D formatting. Same reading = same meaning.

---

## Summary of build changes

| file | change |
|---|---|
| `recreated_pptx/build/slide_004.js` | WHERE_LINES facts: `→` → `⇒` (3 occurrences) |

Nothing else changed. No equation PNG re-rendered, no second Remember box added,
subscript case unchanged.
