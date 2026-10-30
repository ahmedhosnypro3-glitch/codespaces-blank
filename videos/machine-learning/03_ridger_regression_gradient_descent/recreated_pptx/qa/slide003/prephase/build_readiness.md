# build_readiness — slide 003 (S20a prephase, pool run 299640)

Readiness verdict: **READY TO BUILD/FIX** — the build (attempt 8) is structurally complete
and matches the original on every PIL-verified element; remaining work is 6 vision-gated
resolutions (below) plus small color/geometry patches they may trigger. No structural
rebuild is expected.

## Certified components to reuse (do NOT re-derive)

1. `shared_patterns/house_chrome.js` + `house_chrome_check.py` — already consumed
   (`drawHouseChrome(pptx, slide, {numeral: 3})`). Run `house_chrome_check.py` on every
   150dpi render BEFORE judging (deck law).
2. `recreated_pptx/build/slide_007.js` (CERTIFIED) — idioms to copy when touching text:
   multi-run colored addText, per-line separate addText (pptxgenjs v4 law: breakLine emits
   no <a:br/>; nested-array paragraphs make LO drop the shape), charSpacing fit instead of
   font-size changes for overlong lines.
3. `recreated_pptx/qa/slide003/parens/arc_*.png` — cut from the original (yvec, wvec,
   matrix, midcol). If #17 (matrix right paren) resolves as a wide curve, cut a NEW wider
   arc from the original region x355..400 y360..490 instead of stretching the current one.
4. Equation assets: none needed (all 003 math is native text runs; `eq_003_remember.json`
   sidecar is written by the build for the post-cert OMML pass).
5. pptxgenjs gotchas already encoded in the build (keep them): lineSpacing in POINTS;
   per-entry text boxes because LO ignores lineSpacing on inline runs; explicit px() frame
   coordinate law (1px=1pt).

## Build checklist (delta row → concrete action)

| Delta row | Action |
|-----------|--------|
| #1 chrome | none — module in use; run house_chrome_check.py on next render |
| #2 title | none pending `desc_full` (one-line 23pt already guaranteed by box width) |
| #3-#12, #14, #22-#25 | none — PIL-verified matches |
| #8 top y-labels | if `desc_topbox` shows band-colored y1/y2/yn (yellow/cyan/pink), recolor the three runs at y274; else keep red |
| #13 y-vector chips | PIL-SETTLED 2026-10-25: the original carries CHIPS behind the y-entries — yellow x~110..133 y368..390 (y1), cyan y397..423 (y2), pink x~110..135 y456..478 (yn); dots row and w-vector are chip-free; entry text is DARK on the chips. Action: ADD 3 chip rects (sample exact hues from the FFFF99/CCFFFF/F0A0F0 families) behind the entry runs and recolor those runs dark (000000-family per crop); keep dots row + w-vector as-is (w-vector white, PIL) |
| #17 5th column / paren | after `desc_matrix`: (a) if rows end "… x1d", verify the build's 5th cell position against the transcript's slide-space bbox (build places it x365 — INSIDE the paren bulge zone; adjust if the transcript disagrees); (b) if the paren is a wide curve, cut a wider arc PNG from x355..400 y360..490 and place it to trace the measured curve; then DELETE the stale "right curve x358..368" comment conflict by updating the build comment to the measured extent |
| #18/#21 dim labels | if `desc_matrix` shows letter "x" (not "×"), change "N × 1" → "N x 1", "N × d+1" → "N x d+1", "d+1 × 1" → "d+1 x 1" |
| #19 red micro-ink | RESOLVED 2026-10-25 — the micro-ink is JPEG chroma fringing around the purple "N × 1" label (label ink x141..162 y466..475); NOT an element. No build action; do not add anything |
| #20 w-entry colors | if `desc_matrix` shows w1 red (attempt-21), split the w-vector color map: b red, w1 red, w2..wd blue — or whatever the transcript reports; build currently colors all w-entries blue — **PROBE NOTE (pil_probe_003.txt §3): build's b is already red bold and the frame confirms it (entry-1 row: 84 red px, 0 blue); only w1's color is open — do not touch b** |
| #23 stale comment | one-line comment fix in slide_003.js header ("x572..752" → x585..886); code already correct |

## Pre-dispatch state (honesty note)

- 15 ground-truth legs planned for 003/004/005; gateway saturated (load 13-22) through the
  window. All 15 legs are owned by three persistent supervisors (this run, pids
  256045/256049/256055, 6h deadline, dispatch only when gateway load < 8 per the yield law;
  earlier single-shot packs superseded). This doc's [?] items resolve the moment the
  transcripts bank as `orig_judges/desc_<leg>.txt`.
- No certification judge was run by this worker; all rows above are PIL-first evidence.
