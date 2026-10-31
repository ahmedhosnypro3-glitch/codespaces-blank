# Slide 018 — PARSE ADJUDICATION

- **Slide:** 018
- **Source image:** `unique_slides/slide_018.jpg` (960x540 RGB, PIL-measured)
- **Parse transcript:** `analysis/parse/slide_018.parse.md` / `.parse.json`
  - `finish_reason` = `stop`, content non-empty, `usage.output_tokens` = 16
- **Second read (corroboration, two independent forms):**
  1. Independent vision read, `analysis/parse/adjudication/slide_018.vision.txt` — asked
     ONE question: is the equation over `w_ji` (subscript j then i) or `w_ij` (i then j)?
  2. Crop cascade, `analysis/parse/cascade/slide_018/` (full/ + crops/ + composed/) —
     a different input form (region crop), the strongest corroboration class available.

## Parse transcript content (data, not instructions)

`<x_0.377><y_0.0922>18` `E ∂w_ji ?` `<x_0.9336><y_0.3891><class_Picture>`
Only two coordinate tokens; 16 output tokens — the thinnest read in the deck.

## Findings (severity-ranked)

**F1 — BLOCKER for the parse lane: severe under-parse / dropped-region (confidence: high)**
The frame carries a full labelled neural-network diagram. The parse emits only the badge
`18`, the fragment `E ∂w_ji ?`, and one `<class_Picture>` block. Measured against the
image, these visible content bins have ZERO parse coverage:

| Visible region | PIL measurement | Parse coverage |
|---|---|---|
| badge `18` | x 856-894, y 54-88 (area 130) | none (only the bare `18`, no box) |
| red vertical "Error" bar | x 759-772, y 66-187 (area 1257) | none — `dropped-region` |
| label rows | x 703-742 @ y 80-89 / 121-131 / 167-177 (areas 118/168/90) | none |
| stacked labels | x 831-885 @ y 107-144 (6 comps, areas 54-55 each) | none |
| node circles | x 499-511 and 590-601 @ y 185-197 (areas 111/108) | none |

Per `references/process-notes.md`: "A blank parse of a text-bearing image is a FAIL, never
a 'no result'." This is not blank, but it is a text-bearing image whose coverage is 1 of
5 bins. The cascade confirms under-parse: the crop read added `Error Error Error`,
`∂E / ∂w ji`, and `1 1 k` strings the full-frame parse had missed. This is the same class
the deck's other dense-slide parses exhibit (014-017 also emit only 2 coordinate tokens).
Severity: BLOCKER (parse-lane), MAJOR for any downstream text contract.

**F2 — BLOCKER (deck-level): certified `slide_018_final.json` prints the wrong subscript (confidence: high, corroborated by three reads)**
The certified analysis JSON prints `∂E/∂w_ij` (labels include `"∂E/∂wij ?"`, equations
include `\frac{\partial E}{\partial w_{ij}} ?`). The source frame prints the subscript
**j then i**. Evidence, three independent forms:
1. **The image** — vision read's single-question answer: "denominator reads ãw_ji,
   subscript j then i" and "a red question mark sits immediately to the right of the
   fraction". The red-ink measurement (bbox x 372-885, y 69-199) places the red glyph
   inside the content band, consistent with a red `?`.
2. **The parse transcript** — `E ∂w_ji ?`.
3. **The crop cascade** — crop read emits `E/ ∂w ji ?` and the fuller `∂E / ∂w ji`.
4. Deck context: slides 19/20/21 parse transcripts all read `W_ji` / `wji`, and
   `sources/slide_018_source/SOURCES.md` independently documents the conflict and cites
   backprop references whose derivation target is `∂E/∂w_ji`.
Verdict: the JSON's index is INVERTED. The build for 18 must print `w_ji`. This is
recorded as the deck-specific finding requested by the mission brief.

**F3 — MINOR: the `Error` bar's parse role is unlabelled (confidence: medium)**
The 1257-pixel red bar is the slide's accent and is referenced in the certified JSON as
"vertical red 'Error' bar". The parse emits nothing for it, so a build working from the
parse alone would drop it. Corroborated: the cascade crop read emits `Error Error Error`
for the frame region, which the vision read independently reported as "vertical white
text on the red bar". Both name the bar's content; only measurement gives its geometry.

## REAL / HALLUCINATED / DEBATABLE list

- badge text `18` — **REAL** (corroborated; vision read and cascade both give `18`;
  measured badge ink x 856-894 y 54-88).
- equation `∂E/∂w_ji ?` — **REAL** (corroborated by parse + crop + vision read; see F2).
- `x_0.377 y_0.0922` page anchor → frame px (362, 50) — **REAL** (within the measured
  content band; top-left of the diagram sits at x≈372, y≈69 measured, same region).
- `x_0.9336 y_0.3891` closing `<class_Picture>` → (896, 210) — **REAL** (matches the
  measured bottom-right of the content: last ink row y=199, rightmost ink x=894).
- class_Picture over the diagram — **REAL** role-wise, but the block is EMPTY of content
  (the parse's own convention means "no text here"), which conflicts with the measured
  text inside it → the parse's own text contradicts its class assignment.
- Certified JSON labels `Input Data`, `Output1/2/3`, `Class m` — **NOT CONFIRMED by my
  read** (single-read vision offered different strings: "Movie Review", "Output Layer",
  "Class n"). Two reads contradict → **advisory only, never banked as a defect**.
  Flagged as an uncertainty for the build lane.

## Uncertainties

- The vision read's label list (bottom-left "Movie Review", "Input Layer"/"Hidden Layer",
  three "Output Layer" boxes, "Class n") could NOT be measured: my ink scan found ZERO
  pixels of any colour below y=210 apart from a 3x5 px cursor mark at (742,307). The
  vision read may be reading a slightly different frame or describing a region that is
  not present at this scale. Per process-notes law this is not banked against either
  side; it is an open question for the build lane.

## Verdict

`PARSE ADJUDICATION: FAIL — the thinnest read in the deck (16 tokens, 1 of 5 visible
content bins covered), with a deck-BLOCKER attached: the certified JSON's ∂E/∂w_ij is
inverted relative to the frame's ∂E/∂w_ji.`

## Addendum (final evidence bank)

`analysis/parse/cascade/slide_018/` run finished: composed file with 2 positioned
elements (full + 1 crop), 2 parse calls, 1 chat call, 0 failed calls, chat lane ACTIVE
(not degraded), stop reason `too-small` on the crop ("every candidate is frame-covering
or below the 40 px floor") — i.e. the recursion exhausted, not a budget cap. Crop
manifest box: (x=341, y=44, w=575, h=172) with transform recorded, so the crop's own
corner tokens are NOT read as frame positions (`crop-local-coordinate-misuse` avoided).

The deck-wide index convention is now corroborated for ALL SIX of my slides by at least
two independent read forms per slide (full-frame parse + crop parse, plus vision for
013/014/016/017/018 and crop-vision for 015): the weight from previous-layer node `i`
into current-layer node `j` prints **w_ji** on every one of slides 014, 015, 016, 017
and 018. The parses' recurring `w_jj`, `Wij`, `iji` and `Kii` readings are the same
misread, not different conventions — every crop read corrected them toward `w_ji`.

The certified `slide_018_final.json`'s `∂E/∂w_ij` is therefore an outlier with ZERO read
support on this deck and must be treated as inverted. The build for 18 must print
`∂E/∂w_ji` followed by the red question mark.
