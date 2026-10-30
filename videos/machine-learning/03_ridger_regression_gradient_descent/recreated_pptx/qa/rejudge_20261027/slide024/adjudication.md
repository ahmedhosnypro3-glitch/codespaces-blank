# Adjudication — slide 024 CROP FAIL (rejudge_20261027, crop_dense leg)

Adjudicated 2026-10-30, read-only except these notes. No build script, pptx, or DB touched.

## Claim under adjudication

Transcript: `crop_dense_judge.txt` (region slide-space 424,184–728,392, crop 634×434, scale ≈2.0855).

Findings listed in the transcript:

| # | severity | claim |
|---|---|---|
| 1 | MAJOR | Original title carries text before "Descent" (allegedly "Gradient"); render title starts flush with "D", so the whole heading block sits ~50–60 px left of the original |
| 2 | MINOR | render heading red deeper/darker than original's brighter red (confidence low) |

FINAL VERDICT in transcript: FAIL (title content incomplete / mis-positioned).

## Ground truth

- `recreated_pptx/build/slide_024.js:54` — `const TITLE = "Gradient Descent (GD)";` rendered centered in a 640-px box at ink target x 242..718, y 224..268.
- `analysis/slide_024_final.json` — `slide_title` = `"Gradient Descent (GD)"`.

## Pixel evidence (PIL, red-ink mask r>120, r−g>60, r−b>60)

Full images, title band slide-space y 222..270:

- ORIG `unique_slides/slide_024.jpg` (960×540): 3 word clusters at x **242..423** (w 182), **440..609** (w 170), **625..718** (w 94); ink rows 220..271. (Runs at x 59 and 901 are the house red frame strokes.)
- RENDER `render.png` (2001×1125, scale 2.0844): 3 word clusters at slide-space x **240.4..422.2** (w 182.3), **438.5..609.3** (w 171.3), **624.6..717.7** (w 93.6); ink rows 219.7..271.1.
- Word count, word positions, word widths, and vertical extent match within 1–2 slide px. The first word — present in both at identical geometry — is "Gradient" (8 glyphs; cluster counts equal at gap≥2 slide px). If the render had dropped "Gradient", its first word would be "Descent" (w ≈170) starting at x≈242; instead the render's first word is 182 px wide exactly like the original's.

Crop pair itself (both 634×434, same scale):

- Title-band leftmost red ink in BOTH `crop_dense_render.png` and `crop_dense_orig.png` is at crop x ≈31–33 → slide x ≈439–440, i.e. the "D" of "Descent". Crop x 0..30 contains background only in the render; in the orig the only non-background pixels in x 0..31 are the antialiased left edge of that same "D" at x=31 (colors like [202,61,60] fading from [230,211,214]). There are NO clipped glyph fragments left of the "D" in the original crop — the crop's left edge (slide x 424) falls in the inter-word gap after "Gradient" (which ends at x 423), outside the crop in both images.
- Title-band ink-column IoU render vs orig = **0.94** (474/504 columns); the 30 non-shared columns are 1-px antialiasing edges on both sides, not content.
- The "~50–60 px left shift" of the `and` / `minimize …` lines claimed in the transcript is likewise not supported: those lines are centered on their own measured ink centers in the build (S1 ink x 451..508, S2 ink x 201..759) and match the original's measured ink extents.

## One gate vision leg (title-band zoom, matched scale)

`title_band_render.png` vs `title_band_orig.png` (slide-space x 190..790, y 214..282, both 1250×141) via 16_vision_gate.sh, transcript `title_band_vision.txt`:

- Reads both as **"Gradient Descent (GD)"**, identical wording/capitalization, no missing/garbled glyphs — "No content errors … String is identical".
- Only MINOR cosmetic differences (red hue, ~10–15% cap-height, tracking, paren thickness), several attributable to JPEG capture.
- FINAL VERDICT: **PASS** for the title band.

## Dispositions

- **Claim 1 (MAJOR, missing "Gradient" / block shifted left): REFUTED.** Pixel evidence shows "Gradient" present in the render at the original's position and width; the alleged clipped fragments at the orig crop's left edge do not exist (crop edge cuts the inter-word gap; both crops' title ink starts at the "D" of "Descent"). The transcript's reading of IMG2 is a misread of antialiasing/JPEG edge pixels. DISMISSED per register rule (vision claim refuted by pixels).
- **Claim 2 (MINOR, red tone): CONFIRMED as a MINOR, advisory only** — consistent with the fresh vision leg's MINOR red-hue note; not a content defect, not a fix trigger.

Net: the crop_dense FAIL for slide 024 is **overturned**; slide 024's certification stands. No fix dispatched.
