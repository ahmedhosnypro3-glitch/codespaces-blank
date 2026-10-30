# Adjudications — slide 023 crop-pair eq_zoom (attempt 2, render_2) — VERDICT: PASS

Source: `crop_2_eq_zoom_judge.txt` (Template B, K=2, render_2).
Verdict: **PASS**.

## E1 MINOR — "IMG1 renders λ and I in green; IMG2 shows them in the same dark body ink (no green)"
=> **REFUTED** (pixel proof)

Glyph cores (darkest quartile of each measured ink bbox), ORIGINAL frame:

| glyph | bbox (frame px) | core RGB | G−B |
|---|---|---|---|
| λ | x294..311 y156..179 | (44, 147, 47) | **+99** |
| I | x317..329 y157..178 | (29, 144, 29) | **+115** |
| W (control) | x104..131 y157..179 | (10, 28, 14) | +13 |
| X (control) | x191..210 y157..178 | (8, 27, 12) | +15 |
| X₂ (control) | x230..251 y157..178 | (11, 32, 16) | +16 |

λ and I are strongly green in the original (G−B ≈ +100); every body glyph is
neutral dark (G−B ≈ +15, JPEG ink noise). RENDER_2 λ core is (5,127,5),
G−B +121 — same saturated green, matching the frame. The build's 008000 is the
correct family. The judge itself hedged this finding ("if the source deck itself
highlighted λI in green and only the lecture video desaturated it, this is not a
true defect"). **No build change.**

## E2 MINOR (LOW, "watch item only" — not asserted as a defect) — "exponent '1' may revert to body-black in IMG1"
=> **REFUTED / NON-DEFECT** (pixel proof)

Superscript `-1`, measured bbox x347..363 y150..162:

  ORIGINAL core = (167, 77,  78)   R−B = +89   -> red
  RENDER_2 core  = (161, 31,  28)  R−B = +132  -> red

Both are red; the render's is the more saturated of the two, and both minus and
"1" are red in the render (the composite pastes red `^{-1}` over the black
`^{-1}` from the identical mathtext box). No split exists. **No build change.**

## Outcome
eq_zoom region: **CLEAN** — template-B verdict PASS, both raised items
PIL-refuted. The attempt-1 MAJOR (missing Y underline) is confirmed fixed:
the attempt-2 judge explicitly records "W and Y both carry the underline in each
image (weight/placement consistent)".
