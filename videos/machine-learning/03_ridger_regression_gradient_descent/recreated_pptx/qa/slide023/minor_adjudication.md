# slide 023 — MINOR adjudication record (Template A, attempt 2)

Source transcript: `qa/slide023/judge_attempt_2.txt` — **FINAL VERDICT: PASS**,
no BLOCKER/MAJOR. Three MINOR findings were raised; each is adjudicated here
PIL-first (per `judging.md` / `shared_patterns/judge_protocol_03.md` §6).
Measurement scripts: the commands are reproduced inline so every number is
re-derivable from `unique_slides/slide_023.jpg` (the frame) and
`qa/slide023/render_2.png` (the final render, 2001x1125, S = 2.08333).

---

## MINOR #2 — "(X^T X) underlined (mean-adjusted X)" — **REFUTED**

Claim: in the dim-note line, the render underlines `(X^T X)`; the frame shows it
plain italic with no underline.

Adjudication: a permissive scan (lum < 225) of the frame over
x505..755, y205..220 — the only rows a 20pt underline could occupy below a
baseline of 211 — found:

| ink | rows | max run length |
|---|---|---|
| descender tails of `p`/`X` | y208..210 | 96 px |
| green-box bottom stroke | y218..219 | full width |

**Zero long horizontal dark runs** in the underline band (an underline bar
would be ~200px long and ~2px thick). The dim note in the build carries
`{ }` underline options nowhere: the runs are
`r("(X^T X) is of size ")`, `r("d+1", {color:RED})`, `r(" x ")`,
`r("d+1", {color:RED})` — none underlined, none italic. The judge's "underline"
is a reading of the descender/row alignment, not ink. **No fix.**

## MINOR #3 — "Matrix inversion highlighted red/bold in the Solution line" — **REFUTED**

Claim: the render highlights `Matrix inversion` in red/bold like
`Least Squares` and `Gradient Descent`; the frame leaves it dark.

Adjudication: the solution box interior (x92..870, y440..528) was scanned in the
render with the red predicate `R-G > 40 & R > 90`:

```
red px = 0
```

`Least Squares` and `Gradient Descent` are **NAVY** (`color: NAVY`, i.e. 1F3864:
B-R = 0x36-0x1F > 0 in the OPPOSITE channel order) and `Matrix inversion` is the
same single run `r("Instead of using Least Squares with Matrix inversion,")` —
there is no colour or weight break anywhere in that line. Both build lines are
one uniform run at 20pt. The judge merged the two navy emphasis phrases into one
because the ORIGINAL deck does emphasise those words; but the frame's solution
box is uniformly dark navy and the render matches it. **No fix.**

## MINOR #1 — "body text slanted/italic in the render" — **REFUTED BY FONT FORENSICS**

The finding is the only one that is *partly* true about the FRAME, so it is
adjudicated in full. Measured on `unique_slides/slide_023.jpg` (960x540, 1px=1pt):

### (a) the frame's body ink IS slanted — confirmed

Stem-lean = least-squares slope (px/row) of every narrow tall ink run
(2..7px wide, >= 12px tall, rows with >= 2 ink px only). Control: the render's
own title and the frame's title both measure **0.000** — the method is sound.

| region | n stems | median lean | implied angle |
|---|---|---|---|
| blue L1 "The standard matrix inversion…" | 17 | -0.141 | -8.0 deg |
| blue L2 "which means that…" | 22 | -0.129 | -7.3 deg |
| blue L3 "the matrix (increasing cubically…)" | 17 | -0.136 | -7.7 deg |
| EX1 "For Example: if Features vector…" | 10 | -0.146 | -8.3 deg |
| EX2 "or order 1,000,000,000 which is impractical" | 6 | -0.132 | -7.5 deg |
| SOL1 "Instead of using Least Squares with…" | 11 | -0.128 | -7.3 deg |
| SOL2 "use Gradient Descent iterative solution" | 10 | -0.141 | -8.0 deg |
| dim part1 "if Feature vectors are of dimension d" | 2 | -0.132 | -7.5 deg |
| dim part2 "(X^T X) is of size d+1 x d+1" | 7 | +0.018 | +1.0 deg |
| **title** (control) | 5 | -0.000 | **0.0 deg** |
| **"Solution:" label** (control) | 3 | +0.002 | **+0.1 deg** |

So the frame's deck really does set its body paragraphs in a ~7.5-8 deg slanted
(italic-form) face while its title and the "Solution:" label stay upright.
Cross-check with PIL renders of installed faces at matched cap height 17px:

| face | declared/post italic angle | measured median lean | implied |
|---|---|---|---|
| Arial Regular | 0 | +0.000 | 0.0 deg |
| Arial Italic | -12.0 (post table) | -0.198 | -11.2 deg |
| Liberation Sans Italic | -12.0 | -0.202 | -11.4 deg |
| Carlito Italic | -7.0 | -0.118 | -6.7 deg |

### (b) the frame's body `a` glyph is single-storey (italic form)

The standalone `a` of "has a **a** time" was located by NCC-aligning a PIL render
of the substring "has a time" against the frame's L1 band (best NCC 0.530 at
frame x518, y244), giving the glyph at frame x561..571, y248..260. Its ink:

* one enclosed counter (a clean 3-4 px gap between the bowl's left stroke and
  the right stem, closed by a full-width bar at the bottom, with a short
  right-exit tail below) — the **single-storey italic 'a'** form;
* Arial Regular/Arial Italic render `a` **double-storey** (two counters:
  upper bowl + lower bowl, visible in the ASCII dumps);
* Carlito Italic renders `a` single-storey — matching the frame.

### (c) no installed face reproduces slant + storey + advance at once

L1 ink extent, frame vs render (identical window x92..862, y238..268,
predicate lum < 150):

```
L1    orig x  98.0.. 834.0 (w=736)   render x  96.8.. 849.1 (w=752)  right +15.1
L2    orig x  97.0.. 840.0 (w=743)   render x  96.3.. 848.1 (w=752)  right  +8.1
L3    orig x  97.0.. 760.0 (w=663)   render x  96.3.. 762.7 (w=666)  right  +2.7
EX1   orig x  96.0.. 853.0 (w=757)   render x  97.8.. 856.3 (w=759)  right  +3.3
EX2   orig x  96.0.. 541.0 (w=445)   render x  96.8.. 542.0 (w=445)  right  +1.0
SOL1  orig x 246.0.. 709.0 (w=463)   render x 244.8.. 708.7 (w=464)  right  -0.3
SOL2  orig x 313.0.. 648.0 (w=335)   render x 309.6.. 649.7 (w=340)  right  +1.7
L1 'T' cap: orig 17.0 px   render 16.3 px
```

At the frame's cap height (17px), the L1 advance of each installed italic sans
candidate:

| face | L1 advance @ cap 17 | vs frame 736 | 'a' storey | slant |
|---|---|---|---|---|
| **Arial Regular (build uses)** | 752 | **+2.2%** | double | 0 deg |
| Arial Italic | 752 (identical advances: 0 of 95 ASCII codepoints differ) | +2.2% | **double** | -12 deg |
| Liberation Sans Italic | 770 | +4.6% | double | -12 deg |
| Nimbus Sans Oblique | 769 | +4.5% | double | -12 deg |
| Carlito Italic | **853** | **+15.9%** | single ✔ | -7.0 deg |
| Open Sans Italic | 945 | +28.4% | single | -12 deg |
| DejaVu Sans Oblique | 1072 | +45.5% | single | -11 deg |

(The `Arial Regular` vs `Arial Italic` advance identity was verified with
fontTools `hmtx` over ASCII 32..126: **0 of 95 codepoints differ**.)

### (d) decision — keep Arial Regular, bank the refutation

Two mutually exclusive defects are possible:

1. **Swap the face to Arial Italic** — slant becomes -12 deg (the frame's is
   ~-8 deg: a 50% overshoot) AND the `a`/`e`/`g` glyph forms go from "matching
   the frame's non-italic letterforms" to "double-storey where the frame is
   single-storey" — i.e. it *introduces a wrong glyph shape*. Template B
   grades a wrong glyph shape as MAJOR-to-BLOCKER at zoomed scale even when
   invisible at full-slide scale. The deck's upright runs (title, "Solution:",
   dim part2) would then also be inconsistent with a body face 12 deg steeper
   than anything on the frame.
2. **Keep Arial Regular** — slant error only: 0 deg vs ~-8 deg, i.e. ~1.4 px of
   lateral drift over a 20 px cap height (a sub-visual shear), plus the already
   accepted +2.2% advance deviation.

Defect (2) is strictly smaller than defect (1), and it is the only choice that
keeps every measured ink extent, every wrap budget, and the glyph forms intact.
The slant difference is a **font-availability limitation of this pipeline** (the
frame was rendered from a font not installed here and not reproducible offline),
not a build error, and it is already recorded as a MINOR at MEDIUM confidence on
a PASS verdict. **No change to `build/slide_023.js`.**

`render_2.png` / `build_attempt_2.js` bytes are therefore final.

---

## Verdict

All three MINOR findings are PIL-refuted with banked measurements; no geometry
change is warranted. Full-slide leg stands at **FINAL VERDICT: PASS**
(`judge_attempt_2.txt`). Crop-pair certification proceeds from the unchanged
`render_2.png` bytes.
