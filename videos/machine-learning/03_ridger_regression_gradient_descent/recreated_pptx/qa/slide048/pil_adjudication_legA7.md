# PIL adjudication — slide 048 leg A attempt 7 (render_9)

Judge transcript: judge_attempt_7.txt (FINAL VERDICT FAIL, 7 findings).
All seven adjudicated against frame pixels (orig `unique_slides/slide_048.jpg`
960×540 vs `render_9.png` 2001px, ×2.0833 → frame). **No fix triggers; build
current at render_9.**

1. **Stray "x" glyphs in/around every column vector and equation (MAJOR 0.95)** —
   REFUTED (fourth repeat of the same misread; refuted 3× in
   `pil_adjudication_legA6_crop8.md` §legA6-1 and in the crop adjudications).
   The mathtext sources (`gen_assets_048.py`) contain no x/k glyph anywhere;
   content pixels of render_9 are identical to the attempt-4-PASSed render
   except the intended underline/label fixes. At crop scale the judge reads
   bracket strokes + sub-pixel fragments as "x".
2. **Vector delimiters bars | | instead of parentheses ( ) (MAJOR 0.90)** —
   REFUTED. Frame census shows the delimiter strokes are CONTINUOUS VERTICAL
   RUNS (straight strokes), not curved parentheses; the build's 1px-rect idiom
   matches. Consistent with the tall-stroke census in
   `pil_adjudication_crop5_top_band.md` §2 (orig cols 641/647-651/655-656/664-665/
   669-670/678/686-687/695/700; render 644-650/667-672/693-694) — the render
   carries the same straight delimiters as the original.
3. **Z₁/Z₂/Z₃ table missing middle row (MAJOR 0.90)** — REFUTED
   (`scratch/s7_048_adj7.py`, output banked `scratch/s7_048_adj7_out.txt`).
   Dark-px row census x637..706: RENDER has THREE bands — frame rows 74..83
   (header), 89..97, 105..113; ORIG has bands 72..83 (header) and 90..114 (the
   two data rows MERGED into one 25-row run by the delimiter strokes). Same
   total vertical span (render 74..113 vs orig 72..114), same row count; the
   render actually shows the rows MORE separated than the original. No row is
   missing.
4. **W vector placed before "Initial W =" label (MAJOR 0.90)** — REFUTED (third
   repeat; `pil_adjudication_crop5_top_band.md` §5 frame-pixel maps of BOTH
   images show the identical structure: label band rows 61-74 at cols 366+,
   stacked vector hanging below-left at cols ~330-355 rows 78-102). The vector
   is the mathtext asset `eq_initial_w_col.png` ([4;−2;−2] square brackets),
   matching the original's own layout.
5. **"Top)" overprinted by the X₁…X₆ header (MAJOR 0.95)** — REFUTED
   (`scratch/s7_048_adj7.py`). Aug title/header census x85..235: RENDER title
   band frame rows 147..157 + descenders 160..163, header 169..175 (clearance
   6px); ORIG title 150..156, header 166..174. No overlap in either image; the
   render's title sits 3px higher with clear separation.
6. **Missing red ⇐ arrow after first-row updated W (MAJOR 0.85)** — REFUTED
   (legA6 #4): the orig's red pixels right of box 1 (cols 900-902, rows
   139-196) are a straight VERTICAL border stroke, not an arrow glyph; the
   render has the same stroke.
7. **Comma insertion in "C1 positive, C2 negative,…" (MINOR 0.60)** — REFUTED:
   orig descender blobs at cols ~323-327/357-363 prove the original DOES print
   the commas (legA6 #4b).

Conclusion: 7/7 refuted; none is a defect of render_9. Proceed to the three
staged zoomed crop judges (top_band, aug_iter, calc_panel) for certification.
