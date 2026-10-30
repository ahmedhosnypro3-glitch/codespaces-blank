# build_readiness.md — slide 042 "Iteration 1" (S20d prephase, 2026-10-25)

Worker S20d · READ-ONLY toward the cert lane's products · evidence:
`delta_vs_related.md` (this dir), `orig_judges/slide_042_stack_desc.txt` (ground-truth
stack transcript, landed 08:35), `orig_judges/crops_manifest.md`, PIL passes banked in
`scratch/tmp/s20d_*.py`.

## Lane state being handed back (parked adjudication, as of 09:33)

- **Attempt 18 live**: render_18 + crop_18 pairs cut 07:32; adjudication_17 fix list
  applied in `build/slide_042.js` (TL channel order, Z1×3 black, LM cell swap); stack
  judge (crop_18) returned **FAIL 07:42**; leg A (full-frame judge) verdict never
  landed — lanes died before it fired.
- **adjudication_16.md** parked with 5/6 FAIL items refuted on PIL evidence; item 6
  (stack content) was left open because the lane had no original-frame read of the
  stack region. **S20d's stack transcript now supplies exactly that evidence** —
  see "Adjudication guide" below. Bottom line: the refutations stand, and the open
  item resolves AGAINST the build's stack content.

## HEADLINE for the lane: the stack needs a content rebuild, not a touch-up

The original frame's five boxes are a **dot-product check sequence**
`d(xᵢ) = |row-vec| (green W col-vec) = value` — NOT the 2-row garbled matrices the
`eq_042_d*/w*` sidecars render. Transcript-verified content (arithmetic self-consistent):

| box | frame content | vs build |
|---|---|---|
| 1 | `d(x₂) = \|1 2 1\| (6,0,0) = 6  ⇒ Keep same Weight  W = (6,0,0)` (digits RED) | build has d(x1) 2-row garble + Update action |
| 2 | `d(x₃) = \|1 1 2\| (6,0,0) = 6  ⇒ Keep same Weight  W = (6,0,0)` (digits RED) | build has d(x2) garble |
| 3 | `d(x₄) = \|1 5 4\| (6,0,0) = 6  ⇒ Update Weight (red ⇒)  W=(6,0,0) − 2*(1,5,4) = (4,−10,−8)  ⇐(red, far right)` (digits BLUE, `− 2 *` BLUE) | build has d(x3) garble; no update equation, no red ⇐ |
| 4 | `d(x₅) = \|1 6 5\| (4,−10,−8) = −96  ⇒ Keep same Weight  W = (4,−10,−8)` (digits BLUE) | build has d(x4) garble |
| 5 | `d(x₆?) = \|1 6 6\| (4,−10,−8) = −104  ⇒ Keep same Weight  W = (4,−10,−8)` (digits BLUE; row-5 subscript [?]) | build has d(x5) garble |

Green (#00A050) 3-row W vectors with tall parens in EVERY box; `W` carries an underline
bar; `= value` black; boxes 1–2 digits red #C00000, boxes 3–5 blue #0000CC.

## Numbered delta→action checklist

1. **Regenerate the five stack equation sidecars** (delta rows 13–15): new mathtext in
   dot-product form per the table above — `d(x_i) = |a\;b\;c| \cdot (w_1,w_2,w_3) = v`
   style with colored runs is NOT reachable in one mathtext PNG → render per-frame
   multi-part images or per-run PNGs (see action 3 mechanism note). Subscripts x₂..x₆.
2. **Green W vectors + tall parens as separate colored parts**: one green mathtext PNG
   per box for `(6,0,0)` / `(4,−10,−8)` (3-row column, tall parens), reuse the 041-cert
   P3 paren mechanism (`qa/slide041/assets/parens041/`) or 042's own
   `render_stackeq_042.py` extended to color runs.
3. **Box 3 update equation as its own PNG**: `W = (6,0,0) - 2*(1,5,4) = (4,-10,-8)` with
   black W-paren group, blue `- 2 *`, black `(1,5,4)`, green result — again split by
   color into stacked PNG parts placed at transcript x-positions (655..751), plus the
   red `⇐` glyph at x771..791.
4. **Decision arrows/actions**: black `⇒` + "Keep same Weight" boxes 1/2/4/5; RED `⇒`
   + "Update Weight" box 3 (delta row 13). Remove the banked red-Update/black-Keep
   mapping that says box 1 = Update.
5. **Drop the green ⇐ x380 glyphs and the per-box lineB W PNGs** (delta row 14) — the
   frame has no per-box W-update line except box 3; the x380 zone holds the green
   vector's left paren instead (F4 arbitration).
6. **Keep**: cream top box, TL table (txtsub runs, attempt-18 fix), TL class row + red ⇒,
   LM caption + 4-band LM table (no header — frame-verified), Iteration 1 badge,
   5-box borders at banked tops y217/273/340/406/472 (transcript box bounds are the
   coarse vision estimate; banked PIL wins).
7. **RESOLVED [S20d-vision topband] — port 041's legend verbatim**: the 042 frame's
   legend is glyph-identical to the certified pattern — C₁ RED ≈x239, " positive, "
   black italic, C₂ BLUE, " negative, " italic, Zero GREEN bold-italic, " is
   unaccepted" black. DELETE the build's ⇒ at x239..253 (that ink is the legend's C₁)
   and the black C1 at x257; port 041's fragment positions/colors as-is.
8. **RESOLVED [S20d-vision topband] — Initial W = (4, −2, −2) THREE digit stacks**
   (y≈59/75/93, same rows 043/044's frames show): add the third stack, realign the two
   existing, and port 041's P3 paren mechanism for the W vector. The banked two-stack
   reading and the red ⇒ were misreads of the legend row (delta row 4).
9. **RESOLVED [S20d-vision topband] — TL and Z columns carry tall shared parens**:
   port 041's P3 paren PNGs for all six TL columns and the three Z columns (keep
   Z1×3 black; Z subscripts ambiguous at glyph level — 041-cert's Z1×3 stands). The
   build currently draws no TL/Z paren glyphs at all.
10. **ADD frame box 1 — the `d(x₁)` row** (S20d PIL discovery; delta row 16):
    `d(x₁) = \|1 1 1\| (4,−2,−2) = 0 ⇒ Update Weight, W = (4,−2,−2) + 2*(1,1,1) =
    (6,0,0)` — box top border y139, bottom border y198..201, content ≈ y150..195.
    Red `\|1 1 1\|`, green vectors + tall parens, red `+ 2*`, red `⇐` far right, black
    `⇒ Update Weight`, underlined `W`. The build's five bands stay at frame boxes 2–6
    (no reflow) — this inserts ABOVE band 1. Without it the full-frame judge counts
    6 content rows on the frame vs 5 in the build and FAILS again.
10b. Optional fidelity: the box-7 sliver strip (top border rows y531/534 + white fill,
    delta row 17) — the next table row's border pokes above the slide bottom.
11. **Re-render → house-chrome check → re-judge** per `scripts/17_worker_instructions.md`;
    the re-judge MUST be given the transcript (this dir) so the stack judge reads the
    dot-product form as ground truth, not as a discrepancy.

## Reusable certified components

- `shared_patterns/house_chrome.js` + checker (badge numeral = printed number law).
- 041-cert P3 paren PNGs: `qa/slide041/assets/parens041/` (bowed Bezier parens).
- 042's own `render_stackeq_042.py` (mathtext → 600dpi transparent PNG; extend for
  colored runs / dot-product form).
- txtsub pattern from 041-cert (TL headers/class rows — already ported in attempt 18).
- `\bK\b` payload substitution law for judge prompts.

## Adjudication guide — resolving the parked crop_18 FAIL + adjudication_16

| Parked item | Ruling now armed with [S20d-vision stack] |
|---|---|
| a16 refutations (blue step numbers, results, actions, 3-row vectors …) | Refutations of the *form* claims stand where PIL proved them (F2: no blue at x≤286), but the transcript CONFIRMS the substance the judge saw: 3-row green vectors, `= 6` / `= −104` results, Keep/Update actions as above. Verdict: crop_18 FAIL **UPHeld** — the build's stack content is wrong |
| "blue step numbers" | Re-classify: the colored ink is the red/blue `\|digits\|` (d-vector rows), not step numbers. Fix = action 1 (correct digits+colors), not step labels |
| Item the a16 PIL refuted ("3-row matrices") | Actually TRUE per transcript — a16's refutation was based on the sidecars, i.e. the build, not the frame. Correct the adjudication record |
| Leg A (full-frame) verdict never landed | After the rebuild (actions 1–6 + topband-gated 8–10), re-run leg A + stack judge; hand both the transcript |

## What S20d did NOT do (read-only compliance)

No builds touched, no lane DB writes, no judges dispatched, nothing written outside
`prephase/`. All lane artifacts (render_18, crop_18, adjudications, sidecars) untouched.
