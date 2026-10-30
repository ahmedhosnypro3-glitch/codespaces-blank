# build_readiness — slide 005 (S20a prephase, pool run 299640)

Readiness verdict: **READY TO BUILD/FIX with one confirmed build defect** — geometry, fills,
borders and every equation ink-box are PIL-verified matches. The Remember-equation X-vs-Y
fork is PIL-SETTLED 2026-10-25 via glyph topology: UPPER eq = Yᵀ… (build correct, no
re-render), LOWER eq = **Xᵀ(XW)=(XW)ᵀY** (build's Y-first PNG is wrong — re-render required).
Remaining open work is per-token styling plus the re-render, both mechanical.

## Certified components to reuse (do NOT re-derive)

1. `shared_patterns/house_chrome.js` + `house_chrome_check.py` (numeral 5) — in use.
2. `recreated_pptx/build/slide_021.js` (CERTIFIED) — the 600dpi equation-PNG ink-box
   placement law and the multi-color per-segment composition pattern
   (`qa/slide021/compose_eq_021.py`); needed if #4 (red ½) or #13 (Xᵀ string) require
   recomposed PNGs.
3. `eqFit()` ink-box placement (slide_005.js lines ~111-124) — fit-to-ink law; keep using it
   for any re-rendered equation.
4. The nine `eq_005_*.png` + `.json` sidecars; `scripts/render_eq.py` for re-renders
   (matplotlib mathtext, 600dpi, transparent, 8px pad — sidecars carry pad_px/dpi).
5. Attempt-9 noise law (encoded in build comments): eq5's original ink ends x637; never
   re-stretch toward x683 (JPEG noise). Any re-measurement must reject columns with <3 ink
   rows.

## Build checklist (delta row → concrete action)

| Delta row | Action |
|-----------|--------|
| #1-#3, #5, #6, #8-#12, #14-#16 | none pending desc evidence — PIL-verified matches; geometry frozen |
| #4 red ½ | after `desc_eq_stack` confirms: recompose eq_005_loss1.png with a RED ½ (per-segment mathtext via the slide_021 compose pattern), same ink box (98..544 × 109..150), update sidecar color note; re-run OMML-sidecar consistency at wrap time — **PROBE NOTE (pil_probe_005.txt): the asset ALREADY renders the red ½ (PIL-verified 2026-10-25; frame red cluster x150..169; eq2/eq3 zero red = all-black assets correct). Verify the transcript agrees, then at most update the sidecar color note; recomposing from the sidecar (color 000000) alone would DROP the red ½. For the OMML manifest, loss1 needs a red run for the ½ or the PNG fallback** |
| #7 blue-upper Remember | X-vs-Y PIL-SETTLED 2026-10-25: upper first glyph = serif Y → current eq_005_remember1 is CORRECT; fork (a) is CLOSED — do not re-render for X. Remaining after `desc_blue_upper`: (b) apply per-token colors/bold/underline exactly as the transcript reports (current build: X red, W 3736BB underlined, XW underlined); (c) if the transcript shows different token emphasis (e.g. XW bold, "vector" underlined), re-split the runs — never reword |
| #13 lower Remember | PIL-SETTLED 2026-10-25 (glyph topology): original lower = Xᵀ(XW)=(XW)ᵀY; the current PNG (Y-first, sidecar fs 24.4) is WRONG — re-render eq_005_remember2.png via scripts/render_eq.py with `X^{T}(XW) = (XW)^{T}Y`, re-place via eqFit at ink box x660..867 y395..420, update the sidecar mathtext; this closes the attempt-11 legA MAJOR (`desc_lower_eqs` then only verifies styling/glyphs) |
| #9 pink band | build already draws W red bold; if `desc_pink_band` adds more (e.g. "Best" also styled), re-split runs accordingly |
| any re-render | after each PNG change: re-render 150dpi slide, run house_chrome_check.py, re-run the zoomed crop-pair judge for the touched region per judge_protocol_03.md before re-certification |

## Pre-dispatch state (honesty note)

- 005's five legs dispatched via this run's pack (`run_pack.sh full eq_stack blue_upper
  pink_band lower_eqs`, probe law). [transcripts pending at doc write time — gateway
  saturated]. All rows above rest on PIL evidence + banked attempt-11 findings; no claim
  here depends on an unbanked transcript.
- No certification judge run by this worker.
