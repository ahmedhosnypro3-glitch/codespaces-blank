# build_readiness.md — slide 044 "Perceptron iteration 3" (S20d prephase, 2026-10-25)

Worker S20d · READ-ONLY toward the cert lane's products · evidence:
`delta_vs_related.md` (this dir — now carries the full [S20d-vision stack+topband]
arbitration + per-band ground-truth table), PIL passes in
`scratch/tmp/s20d_prephase_pil_043_044.py`, `s20d_prephase_pil_refine.py`,
`s20d_prephase_pil_044extra.py`, `s20d_prephase_pil_zero.py`, `s20d_prephase_pil_redshape.py`,
`s20d_prephase_pil_044stack.py`, `s20d_prephase_pil_044stack2.py`, ground-truth reads
`orig_judges/slide_044_stack_desc.txt` + `orig_judges/slide_044_topband_desc.txt`
(both landed 2026-10-25), and the 042 stack transcript
(`../slide042/prephase/orig_judges/slide_042_stack_desc.txt`).

## Lane state being handed back

- The build was promoted to `slide_044_recreated.pptx` v2 (banked 00:04) but the
  lane's judge legs never fired (attempts 0 in the mission DB) — this pack is the
  fast-start input.
- **Rebuild blocker (must clear first)** — two stacked defects:
  1. `slide_044.js` `eqImg` passes the sidecar's `path` field straight to addImage;
     all 14 `eq_044_*.json` `path` fields are dead `/workspaces/codespaces-blank/...`
     absolutes.
  2. The PNG files themselves are **absent repo-wide** (only 042's w-PNGs exist).
  Any rebuild fails. The banked pptx is unaffected.

## HEADLINE: regenerate the asset set, then the content questions — ALL now arbitrated

Same structural story as 042/043 (cross-slide decode in `../slide043/prephase/build_readiness.md`
and the 042 delta doc): the sidecar mathtext is the flattened dot-product garble —
dx1 `d(x_1) = [1 \; 1 \; 1; \; -12; \; -8] = -12` decodes to
`d(x₁) = |1 1 1| (8,−12,−8) = −12` (043's final W; arithmetic ✓) and w1 decodes to
`W = (8,−12,−8) + 2*(1,1,1) = (10,−10,−6)`.
**The 044 stack + topband transcripts have since LANDED and are PIL-arbitrated** — every
VERIFY item below carries a verdict, and `delta_vs_related.md` ("[S20d-vision
stack+topband] ARBITRATION") holds the per-band ground truth: update rows = boxes 1–3,
family W-line colors with RED `+ 2 *` (PIL-confirmed), red ⇐ on the three update rows,
legend Zero GREEN, TL two data rows, tall TL/Z parens, box 3's missing bottom rule
y≈329.5, and the frame's own `−112` typo in box 6 (recreate as printed).

## Numbered delta→action checklist

1. **Port `qa/slide044/gen_assets_044.py` to this host** (it hardcodes the codespace
   DECK and RENDER paths), then **rewrite its EQS mathtext in dot-product form** per
   [S20d-vision stack] and regenerate all PNGs + sidecars with repo-relative `path` +
   bare `image` field.
2. **Fix `eqImg`**: `path: ASSETS + m.image` (043's safe pattern), not `m.path`.
3. **Legend fix (2 bugs) — CONFIRMED [S20d-vision topband]**: split the single multi-run
   addText into 041-cert per-fragment boxes, and color **Zero GREEN** — the topband read
   gives the exact pattern: C₁ RED x≈239 / "positive," italic / C₂ BLUE x≈315 /
   "negative," italic / Zero GREEN bold x≈398 / "is unaccepted" black. Multi-run addText
   is the exact pattern 042 proved breaks run colors in LO renders.
4. **TL/Z mechanisms — RESOLVED [S20d-vision topband + PIL]**: port 041's txtsub for
   headers and class rows; port 041's P3 tall paren PNGs for the six TL columns AND the
   three Z columns (transcript: tall thin parens both groups). Use PIL column centres —
   TL ≈ 96/118/140.5/163/185.5/208.5 and Z ≈ 605/627.5/648..650 (both = 041-cert
   identity). **Do NOT use the transcript's absolute x-positions** (locally drifted up to
   +32px on Z); transcript is authoritative for content/colors only.
5. **W-line colors rows 1–3 — RESOLVED [S20d-vision stack + PIL]**: the update-band W
   lines are NOT all-red. Family form per band: black `W̲ =` (underline bar) + black
   old-W column + **RED `+ 2 *`** (PIL: 13/6 red px, 0 blue — transcript [?] resolved
   red; NOTE 042's subtract-update prints BLUE `− 2 *` — per-frame/per-sign difference,
   both PIL-confirmed) + black x-column + GREEN result. Regenerate w1..w3 as multi-part
   colored PNGs; w4..w6 are the short black `W̲ = (14,−4,0)` group only (Keep rows).
6. **Far-right ⇐ in update bands — CONFIRMED [S20d-vision stack + PIL]**: ADD red ⇐ in
   build bands 1–3 (= frame boxes 1–3, the update rows; PIL red px 89/28/0/0/0 across
   the five crop rows at x808..838, transcript x≈815..831; box 1 gets it as an update
   row per family + sidecar decode). Keep rows carry no ⇐.
7. **Keep as-is (frame-verified)**: white calc-area fill (the pattern 043 must copy),
   3-row band structure (y1/y2/y3), class colors C₁ red / C₂ blue (**analysis
   typography swap REFUTED by PIL**), blue LM caption (**analysis "red caption"
   REFUTED** — 596 blue px / 0 red), roundRect Iteration 3 badge, LM text rows,
   Initial-W three stacks (PIL rows y63..101; paren strokes x330+x353 = three-frame
   identity, transcript-confirmed black tall parens; add the W underline bar x319.5..330
   y91.5..93), **decRed rows 1–3 decision coloring is CORRECT** (update rows = boxes
   1–3), no blue arrows (zones hold |digits| ink), no Z-matrix blue box (**analysis
   misread refuted**), mouse-pointer/pencil icon omission (capture artifact —
   transcript confirms the ink at (455.7,342)..(474,360) is a pen cursor).
8. **TL data-row count — RESOLVED [S20d-vision topband]**: TWO data rows
   (1/1)(2/1)(1/2)(5/4)(6/5)(6/6) — build correct; [044-analysis]'s third row REFUTED.
9. **Decision-text placement — ARBITRATED [S20d-vision stack]**: move ⇒ to x≈508 and the
   action text to x≈529..642 (transcript; the build's x333..338 overprints the dx
   cluster). Also fix the calc-area skeleton: ADD the missing box-3 bottom rule at
   y≈329.5 (frame has 12 border rows, the build draws 11 — see the delta doc's "New PIL
   finding").

10. **Regenerate the asset set to THIS spec** (delta doc per-band table is authoritative):
    dx1..dx6 in dot-product form — `d(xᵢ) = |row| (green W col) = value` with RED digits
    boxes 1–3 / BLUE boxes 4–6 (class-colored), GREEN W columns; values: box 1
    `|1 1 1| (8,−12,−8) = −12`, box 2 `|1 2 1| (10,−10,−6) = −16`, box 3
    `|1 1 2| (12,−6,−4) = −2`, box 4 `|1 5 4| (14,−4,0) = −6`, box 5 `|1 6 5| (14,−4,0) =
    −10`, box 6 `|1 6 6| (14,−4,0) = −112` **as printed — the original's own arithmetic
    typo (true −10); recreate verbatim, never correct**. w1..w3 = update equations
    (`W̲ = (8,−12,−8) + 2*(1,1,1) = (10,−10,−6)` / `(10,−10,−6) + 2*(1,2,1) = (12,−6,−4)` /
    `(12,−6,−4) + 2*(1,1,2) = (14,−4,0)`) as multi-part colored PNGs (black W̲-bar group,
    RED `+ 2 *`, GREEN result); w4..w6 = short black `W̲ = (14,−4,0)`. Place per-cluster
    (dx x≈282..458, ⇒+decision x≈508..642, W group x≈634..795, ⇐ x≈815..831) — never
    full-row stretched. Subscripts x₁..x₆ (the box-5/box-6 subscripts resolved by
    elimination + 042 precedent). Write sidecars with repo-relative `path` + bare
    `image` field.
11. **Re-render → house-chrome check → judge legs** per `scripts/17_worker_instructions.md`;
    hand the judges the 042 transcript + this pack + the delta doc's per-band table, with
    the −112-as-printed ground rule so the stack judge reads the typo as frame truth.

## Reusable certified components

- `shared_patterns/house_chrome.js` + checker.
- 041-cert P3 paren PNGs + txtsub pattern.
- `scripts/render_eq.py` + the (to-be-ported) `gen_assets_044.py` sidecar writer.
- The slide's own white-fill calc area (044 v2) — reuse as the deck-wide precedent.
- 042 stack transcript as structural ground truth for the band form.
- 041-cert per-fragment legend pattern (replaces the multi-run addText).

## Judge-payload notes

- Carry the analysis-vs-frame corrections: C₁ red / C₂ blue (not swapped); blue caption
  (not red); no blue box around the Z-matrix; Initial-W has THREE stacks ("[4; −2]" in
  the analysis dropped one); TL table two data rows (topband-resolved); equations are
  dot-product form; box 6 prints **−112** (original's typo, arithmetic −10) — recreate
  as printed; update rows are boxes 1–3 with red ⇒ + red ⇐ + RED `+ 2 *`; Keep rows
  (4–6) carry only the short `W̲ = (14,−4,0)`; every W carries the underline bar.
- GROUND RULES: e-format upgrades are not discrepancies; house chrome disagreements are
  overridden by the house law; the pencil icon in box 3 and the crop-edge red verticals
  are capture/house artifacts, not missing content.
