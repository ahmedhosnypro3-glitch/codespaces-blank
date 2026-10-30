# Attempt 24 adjudication — slide 042 (attempt-25 fix basis)

Worker: kimi-s6-FRESH-1792954337 · 2026-10-25 · deck machine-learning/03_ridger_regression_gradient_descent
Attempt-24 build md5 `5f1350f758b1099716e29f4c5bcb05e8` · render_24 md5 `83280ab5789092e0fa656bb0b9781ab6`.

## Legs dispatched (7)

| Leg | Verdict | Transcript |
|---|---|---|
| legA full slide | FAIL | judge_attempt_24.txt |
| crop stack | FAIL (1 BLOCKER, 3 MINOR) | crop_24_stack_judge.txt |
| crop lm_table | FAIL (1 BLOCKER, 1 MAJOR, 2 MINOR) | crop_24_lm_table_judge.txt |
| crop initial_w | FAIL (2 MAJOR, content PASS) | crop_24_initial_w_judge.txt |
| crop legend | FAIL (1 MAJOR, 1 MINOR) | crop_24_legend_judge.txt |
| crop tl_table | FAIL (1 MAJOR, 2 MINOR) | crop_24_tl_table_judge.txt |
| crop topright | **HUNG** — exit 124, hard wall-clock 1230s exceeded, NO transcript | (see incident below) |

## Incident: topright crop hang

The topright crop judge ran past its hard wall clock (1230 s) and was killed by the
runner (exit 124). No transcript was produced; crop_24_topright_orig/render.png and
the prompt are banked. Decision: do NOT re-dispatch attempt 24's topright leg — the
attempt-25 re-cut round re-judges all six regions (topright included) on render_25,
which also carries the Z-block fix that legA flagged (MINOR #6, mismatched
delimiters). The hang is recorded here as the incident log for that leg.

## Finding-by-finding disposition

### legA (full slide)
| # | Finding | Disposition | Attempt-25 fix |
|---|---|---|---|
| 1 | MAJOR: "−10" wraps into a 4-row vector (rows 5–6) | CONFIRMED (stack BLOCKER #1, twice) | `wrap: false` on tallVec digits; green d-vec x-spans per box (b5/b6 391.3..412.3) so "−10" fits; b4 "= 6" moved 400→406.5 |
| 2 | MAJOR: bracket-fragment delimiters; glyphs sit ON strokes (Initial-W −2 crosses right stroke; bottom "0" Q-collisions rows 2/3/4) | CONFIRMED | bowed paren PNGs everywhere (TL, Initial-W, LM, tallVec, Z), side-aware tip placement, 11pt digits re-centred (341.5/346.5) |
| 3 | MAJOR: legend first symbol reads "G" with arrow-like subscript | CONFIRMED (legend #1: red arrow glued at C₁, sub-1 displaced) | the ⇒ at x239 y109 (TL class-row tail) REMOVED; C₁ alone at x238 |
| 4 | MINOR: "C₂negative," missing space | CONFIRMED | " negative " box at x324 |
| 5 | MINOR: W̲ underline missing rows 2/3/5/6 | CONFIRMED | `wUnderline: true` on all 6 ROWS |
| 6 | MINOR: Z-block delimiters mismatched fragments | CONFIRMED (legA only; dedicated leg hung) | Z digits cx 605.5/628.5/648.5, paren tips (598,612)/(621,635)/(641,655), rp side-aware ink_left |

### crop stack
- BLOCKER #1 (−10 → 4/−1/0/−8 rows 5–6): CONFIRMED → same fix as legA #1.
- MINOR #2 (box1 LHS vec (4,−2,−2) and (1,1,1) "read dark/black" in orig): **REFUTED by
  PIL** — orig box1 d-vec ink (x382..397, y152..192) mean rgb (128.7,159.6,129.5),
  g−r mean +30.9, 10/15 ink px g−r>25 — GREEN, same chroma signature as box2's
  d-vec (g−r +30.2). GREENV retained; (1,1,1) is black in both. No change.
- MINOR #3 (W̲ rows 2/3/5/6): CONFIRMED → legA #5 fix.
- MINOR #4 (brackets vs parens): CONFIRMED → bowed PNGs.

### crop lm_table
- BLOCKER #1 (entire x₁..x₆ header row missing): **CONFIRMED — and the window-1
  refutation is RETRACTED.** The attempt-24 pre-phase refutation scanned band
  y160..166 and found nothing; that was the wrong band. PIL on the original frame:
  y165..175 carries six x-sub clusters at x≈98/120/143/165/188/210 (exactly the
  LM column centres), and the frame's row-clusters are 148..159 (caption) /
  166..175 (header) / 184..222 (digit bands) / 232..234 (class row). Attempt 25 adds
  the header row, moves the digit bands 164/182/197 → 183/198/214 (orig ink rows
  184..191 / 199..207 / 215..222), and adds the white card x70..246 y140..256.
- MAJOR #2 (fragmented bracket stubs): CONFIRMED → bowed paren PNGs, ink y179..225
  (sc = 46/39.96), tips on the 6 pair positions.
- MINOR #3 (no clearance digit-vs-delimiter): addressed by the PNG tips + digit
  centring.
- MINOR #4 (sans vs serif): not counted (ground rule c).

### crop initial_w
- MAJOR #1 (square brackets instead of tall parens): CONFIRMED → bowed PNGs,
  tips 330.5/353.5, ink y62..102 (sc = 40/39.96).
- MAJOR #2 (right delimiter strikes the −2 rows): CONFIRMED → digits 13pt → 11pt,
  boxes re-centred ("4" ink centre 341.5, "−2" 346.5). Render check: digit ink ends
  x350.4, clear of the rp tip 353.5.
- Content PASS (4/−2/−2, η = 2 red italic) — unchanged in attempt 25.

### crop legend
- MAJOR #1 (C₁ distorted, subscript displaced by arrow): CONFIRMED → ⇒ removed;
  render red ink now 238.6..248.7 = C glyph + subscript only.
- MINOR #2 (added commas): CONFIRMED by PIL — orig baseline scans x303..311 and
  x379..394 are EMPTY; attempt 25 drops both commas.
- (Legend item 3 — the "-2" fragment above the legend — was the Initial-W matrix
  seen through the crop window; its bracket-vs-paren concern is fixed by the
  initial_w fix.)

### crop tl_table
- MAJOR #1 (paren delimiters missing on all 6 data pairs): CONFIRMED → 6 bowed
  pairs added, tips (90,102)/(111,125)/(134,147)/(156,170)/(179,192)/(201,215),
  ink y79..104 (sc = 26/39.96); rows re-centred to TL_CX 96.5/118.5/140.5/163.5/
  186/208.5.
- MINOR #2 (comma after "positive"): same legend comma fix.
- MINOR #3 (splayed digit rows): the TL_CX re-centring.

## Attempt-25 build

- All fixes PIL-arbitrated before application; build md5 `7b459f1ae97e3f0d478673f61cbdb6e1`
  (banked as build_attempt_25.js), render_25.png md5 `98bedc4be123bff2f592b6c18edcfd07`.
- house_chrome_check render_25: PASS.
- PIL self-check (scratch/tmp/s6_042_pil25.py): 38/38 checks pass (5 initial fails
  were check-window contamination — digit ink / cream-box border / caption descenders
  caught by over-wide windows; tight-window re-runs all clean).
- Open item carried to the round: the LM card border colour A8B2C2 is an estimate
  from measured (163,169,181)/(195,197,201); render shows exactly (168,178,194) at
  the border, orig darkest sample (195,198,203) — inside the envelope, left to the
  crop judge to arbitrate at matched scale.

## Evidence → fix traceability

tl_table FAIL → build edit 1 (TL parens + TL_CX) · legend FAIL → edit 2 (⇒ removal +
LEGEND array) · initial_w FAIL → edit 3 (bowed parens + 11pt digits) · lm_table FAIL
→ edit 4 (card + header row + bands + bowed parens) · stack/legA FAILs → edits 5–9
(tallVec rewrite, DVEC_XS, W̲ all rows, b4 eqX, Z-block).

## Post-script: B24 DESC corrections carried into B25

PIL red-ink scan of the original frame (this window): the ONLY red ink in the
legend band (x225..570, y95..132) is the C1 glyph itself (x240..251) — there is NO
red arrow anywhere in the TL/legend regions. The B24 `--capture` DESC strings
claimed "red arrow" (tl_table) and "with the red arrow at its left" (legend); the
legend judge explicitly leaned on that claim ("the red arrow that per the region
belongs at the LEFT of the row"). The B25 dispatchers drop the false arrow wording
and name the lm_table header row (PIL-confirmed y165..175) so the judge looks for
it. The frozen `-p` payloads are untouched: all six crop prompts md5
4ce754a2f9515f1f5ac69be4ee0cf04e, legA payload judge_payload_A_23.txt
8fc119623b1f020c6d135c834969bf75, byte-for-byte copies.
