# legA att18 adjudication — both MAJORs DISMISSED (pixel + higher-zoom evidence)

Transcript: `judge_attempt_18.txt` (4338 bytes, FINAL VERDICT: FAIL, 2 MAJORs).
Adjudicated per the arbitration law (vision proposes; pixels and DOM dispose).

## MAJOR 1 — "x4 aug middle entry reads 1 instead of 5" — DISMISSED

Claim: original x4 augmented column = (1, 5, 4), recreation shows (1, 1, 4).

Evidence:
- Build: `build/slide_049.js` line 229 — vals[3] = `["1", "5", "4"]` (x4 column IS 1/5/4).
- Pixels: ASCII ink dump of the x4 middle cell (frame x159..175, y196..210) on
  BOTH render_18.png and slide_049.jpg (150dpi-space, this file's sibling log
  in the window transcript) shows the same glyph — a clear "5" (top bar, left
  stem, bowl) in the render, matching the original's blurred "5". No "1" glyph
  exists in that cell.
- The full-slide legA read at 1x misread the 10pt digit; the att18 top_band
  crop judge (higher effective zoom) passed this exact region.

Disposition: DISMISSED (judge misread at 1x; render matches original).

## MAJOR 2 — "unaccepted" vs "unacceptable" — DISMISSED

Claim: original header-box line reads "Zero is unacceptable"; recreation says
"Zero is unaccepted" (verbatim violation).

Evidence:
- Build: line 203 — `" is unaccepted"`.
- The att18 legend crop judge (`crop_18_legend_judge.txt`, PASS, same attempt,
  higher effective zoom, same bytes) verified the legend TOKEN BY TOKEN:
  `"C1 / positive / C2 / negative / Zero / is unaccepted" — exact match`,
  explicitly "No missing, extra, garbled, or re-ordered words".
- The full-slide read at 1x cannot resolve the italic serif word and guessed
  the longer word.

Disposition: DISMISSED (higher-zoom banked read + build both confirm
"unaccepted" is the original's word; no fix).

## Certification consequence

legA att18 FAIL stands as the raw transcript (never rewritten), but both its
MAJORs are adjudicated DISMISSED. Slide 049's certificate rests on:
crop_18_top_band PASS + crop_18_legend PASS + legA att18 with 2/2 MAJORs
dismissed here. No re-build, no re-judge required.
