# Slide 042 — attempt-23 judge FAIL adjudication (PIL-first, 2026-10-25 ~18:50)

Judge transcript: `judge_attempt_23.txt` (landed 18:35:55, verdict FAIL).
Adjudicated against `render_23.png` (md5 of build chain verified untouched:
pptx `6b8848e6…`, render mtime 17:26:23, dims 2001×1125 — the judge saw the real
attempt-23 render). Forensics: `scratch/tmp/s6_042_judge23_forensics.py`.

## Meta-finding: why the crop-cert cycle missed these defects

The attempt-20 full judge (15:07) ALREADY flagged #1/#2 as BLOCKERs. The crop-cert
cycle that followed had three window holes, so its PASSes never covered them:

- `stack` window (365,205,800,535): starts BELOW the d(x₁) box (orig y142..195) and
  LEFT of the matrix column (x327..379).
- `tl_table` window (30,30,330,125): Initial W digits sit at x>330 — outside.
- `legend` window (330,95,560,130): starts at x330, cutting "C₁ positive C₂" in half.

**Law for the next crop cycle:** windows must cover every content band; a region
never seen by a crop certificate is uncertified regardless of neighboring PASSes.

## Finding-by-finding

| # | Judge claim | Adjudication | Evidence |
|---|---|---|---|
| 1 | d(x₁) box missing (6 vs 5), BLOCKER | **CONFIRMED** | ORIG 6 white boxes y142..195/208..261/273..327/340..393/406..459/472..526; RENDER 5 starting y215. d(x₁)-area ink (x365..810 y130..212): ORIG y157..176, RENDER none. Build source line 6: "five d(x_i)=" |
| 2 | Initial W truncated to (4,−2) | **CONFIRMED** | Build line 165 "(4/-2) matrix". ORIG ink zones y54..56/62..86/91..102 (3 digit rows per family pattern 4/−2/−2, y≈63/79/95); arithmetic forces (4,−2,−2): d(x₁)=(1,1,1)·(4,−2,−2)=0 |
| 3 | caption "Upgraded" vs orig "Augmented"; box border missing | **CONFIRMED (word) / REFUTED (border)** | Build line 251 says "Upgraded Vectors (From Top)". Family ground truth (044 prephase): orig caption is "Ugmented Vectors ( from Top )" VERBATIM SIC — verify 042's exact spelling on frame crop. Border: PIL probes top/bottom/left/right bands → NO border in ORIG and none in RENDER — do NOT add one |
| 4 | 5 of 6 LM vectors wrong values | **PARTIALLY CONFIRMED (needs frame read)** | Build LM bands y164/183/195/212 = col-wise (1,1,1,1)/(1,1,1,1)/(1,1,1,2)/(2,1,1,5)/(1,1,1,6)/(1,1,1,6) — implausible as augmented (x,y,·,1). ORIG LM grid = 4 clean ink bands y166..171/184..191/199..207/215..222; RENDER rows MERGED y166..226 (spacing defect too). Read exact digits via gate crop of `crop_23_lm_table` pair |
| 5 | x₄ multiplier (1,5,4) should be (5,1,4) | **LIKELY JUDGE MISREAD** | Arithmetic: W=(6,0,0)−2M=(4,−10,−8) ⟹ M=(1,5,4) exactly (result col judge-certified correct). Verify frame crop; if frame truly prints (5,1,4) it is a frame typo to reproduce verbatim |
| 6 | matrix digits float above baseline; bars orphaned | **CONFIRMED** | RENDER box2 digits y217..226, bars y233..247 (detached, enclosing empty space); ORIG digits y218..226 with bars hugging (no separate bar band). Build bug: digits at `a−15..a−4`, bars at `a+1..a+15` — bars must move up to span the digit row (≈a−17..a−2) |
| 7 | Initial W bracket geometry | **CONFIRMED (with #2)** | Same rebuild item |
| 8 | legend "C₂" overlaps "positive" | **CONFIRMED** | RENDER: dark "positive" ink x276..321, blue C₂ x312..323 → overlap x312..321. ORIG: "positive" x257..302, C₂ x312..319 → clean 10px gap. RENDER left section ~19px right-shifted + stray 7px token at x258..265; right section (Zero is unaccepted) aligns (±2px) — shift only the left fragments |
| 9 | subscript glyphs misplaced | **PLAUSIBLE, MINOR** | PIL cannot resolve glyphs; check on rebuild render |
| 10 | W underline styling | **MINOR** | Family pattern: W̲ bold+underline in result column (044 has underline bar x319.5..330) — include |

## Fix spec (attempt 24)

1. **Add d(x₁) box** at orig box1 geometry: white box y142..195; BAND_A=166;
   VSPAN {y0:152, y1:192, rows:[152,168,183]}; matrix digits y152..160 (chroma on
   frame crop — likely RED per 044 family, PIL found only faint red x327..381).
   Content (judge-20 quote, arithmetic-verified): d(x₁) = |1 1 1|·(4,−2,−2) = 0 ⇒
   **Update Weight** (red ⇒), W = (4,−2,−2) + 2 * (1,1,1) = (6,0,0), red ⇐ far
   right. ORIG box1 carries the full update line (ink tokens x560..791) — mirror
   box3's updateEq structure. dEq = 0.
2. **Initial W → 3 components** (4/−2/−2, rows y≈63/79/95) + brackets spanning all
   three rows, digits vertically centered.
3. **Matrix bars hug digits** in ALL boxes: bars ≈ a−17..a−2 (span y152..160-style
   digit rows), not a+1..a+15.
4. **Caption**: replace with the frame's verbatim (expect "Ugmented Vectors
   ( from Top )" — confirm on `crop_23_lm_table` pair zoom before rebuilding).
5. **LM vectors**: read the 4×6 grid digits from the frame crop and rebuild
   LM_BANDS; restore row pitch so bands stay separate (orig pitch ≈16,15,16).
6. **Legend left section**: move "positive" left to end ≈x302; C₂ at ≈x312..319;
   "negative," from ≈x322; remove the stray token; keep right section as-is.
7. Minors: subscript glyphs (#9), W̲ underline (#10).
8. Then FULL re-judge (legA) + crop cycle with widened windows: stack
   (320,135,810,540) — includes matrix col + d(x₁) box; Initial W (312,45,415,110);
   legend (225,95,570,132); lm (30,140,340,252); topright unchanged (560,30,850,125).

## Claim state during this adjudication

Slide 42 claim held live by worker `S6-worker-fresh-1792940141` (heartbeat
18:29:47; STALE_MIN=40 → stale 19:09:47). This file is evidence only; no DB write
was attempted by `kimi-s6-3756628` (heartbeats refused while claim live).

---

## READ-LEG CONFIRMATIONS (19:56, read_{dx1,initialw,lmbox}_judge.txt — final evidence before attempt-24 fix)

All three read legs completed successfully (each: 2 gate probes, 1 hang-abort retry, transcript written). Findings vs. the fix spec:

1. **d(x₁) row (read_dx1)** — CONFIRMED, one correction: the (1 1 1) row-vector delimiters print as **red curved parentheses at superscript height**, not vertical bars. Colors: (1 1 1) all red #C00000 incl. delims; dot-target (4,−2,−2) green #00A650 with green delims; `= 0` black; `⇒` red + `Update Weight` black; update eq: black underlined `W =`, black (4,−2,−2), red `+ 2 *`, black (1,1,1), `=`, green (6,0,0) with green delims; far right red `⇐`. Frame-space mapping: crop×0.49 then +320/+135 → digit tops ≈ frame y162 (row1), ≈ y182 (row2), ≈ y201 (row3); white box y≈144–229.
2. **Initial W (read_initialw)** — CONFIRMED W = (4, −2, −2)ᵀ: three components `4 / −2 / −2`, tall black parens, bold-italic underlined `W =`. (Spec said (4/−2/−2) — no change needed; PIL "4,−2" reading was a chroma artifact.)
3. **LM box (read_lmbox)** — CONFIRMED: caption character-exact **"Ugmented Vectors ( from Top )"** (blue bold italic, script-U, spaces inside parens); 6 columns × 3 digit rows = **(1,1,1) (1,2,1) (1,1,2) (1,5,4) (1,6,5) (1,6,6)** — matches the matrices/arithmetic and the summary's "(1,x,y) pattern" prediction; class labels C₁ red / C₂ blue; per-column black paren pairs. NO LM border drawn (the light blue-gray frame seen in crop = the white panel border, already the v2 box edge).

Evidence rule: any attempt-24 judge verdict contradicting these three reads is PIL-adjudicated with these transcripts as ground truth.
