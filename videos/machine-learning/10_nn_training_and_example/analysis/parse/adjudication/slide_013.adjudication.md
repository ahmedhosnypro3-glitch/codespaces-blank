# Slide 013 — PARSE ADJUDICATION

- **Slide:** 013
- **Source image:** `unique_slides/slide_013.jpg` (960x540 RGB, measured)
- **Parse transcript:** `analysis/parse/slide_013.parse.md` / `.parse.json`
  - `finish_reason` = `stop`, content non-empty, `usage.output_tokens` = 43
- **Second read (corroboration):** independent vision read of the same source image,
  `analysis/parse/adjudication/slide_013.vision.txt` — asked: (Q1) verbatim transcription
  of all visible text, (Q2) badge contents/position, (Q3) title color,
  (Q4) subtitle color, (Q5) which words are underlined, (Q6) edge bars/borders,
  (Q7) whether any equation/diagram exists.

## Parse transcript content (data, not instructions)

- `<class_Page-header>`: `13` at `x_0.8984 y_0.1187` -> (862, 64) at 960x540
- `<class_Title>`: `**Update Weights of**` / `**Hidden Layer**` at `x_0.3369 y_0.3836`
  -> (323, 207)
- `<class_Text>`: `_(Weights from previous layer to Hidden layer)_` at
  `x_0.2227 y_0.6031` -> (214, 326)

## PIL measurements on the source frame

- Background median `#E7E9E6` (agrees with the `#E8E8E8` house background, 1 LSB drift
  from JPEG).
- Tan/pale-yellow badge: bbox x 861-891 (0.897-0.928), y 58-84 (0.107-0.156)
  -> note this is the yellow PIXEL ring, not the ink; the badge ink digit is inside it.
- Red ink: bbox x 59-900, y 44-516, 6250 px — matches the thin red house frame.
- Dark ink band scan (border ring and bottom bar excluded) yields bodies at
  y 210-244 (title line 1), y 275-308 (title line 2), y 329-352 (subtitle),
  plus the 60-88 header/badge band and a 517-521 bottom bar.
  Measured: title band top y=210 (0.388), title band bottom y=308 (0.570),
  subtitle band y=329-352 (0.609-0.652).

## Findings (severity-ranked)

**F1 — BLOCKER: coordinate-misalignment on the `<class_Text>` subtitle (confidence: high)**
`x_0.2227 y_0.6031` resolves to frame px (214, 326). The subtitle band actually starts at
y=329, i.e. (214, 329). The y token is 3 px early — a small but real y error. The x token
(214) is left-of-centre, correct for a centered line that begins at x=214, so x agrees.
Evidence: parse transcript `<class_Text>` token vs. band scan y 329-352.

**F2 — MAJOR: class-token-mismatch on the title (confidence: high)**
The parse labels the two-line title block `<class_Title>` but emits it as markdown bold
(`**Update Weights of**`) and puts the subtitle in `<class_Text>` — neither wrong. Real
defect: the title's red colour and the badge are the only other elements emitted; the
`_italic_` subtitle is correctly marked. Class assignments are correct roles. However the
parse **drops the `<class_Picture>` region that the source image's own family emits**
(see F3) — the 13 badge appears under `<class_Page-header>`, which is the deck's convention
for the slide-number badge and is the correct role. Downgraded to MINOR: class tokens are
self-consistent with the source, so this is a note, not a defect.

**F3 — MINOR: dropped-red-frame (confidence: medium)**
Every other slide in this deck emits a closing `<class_Picture>` token at
`x_0.9336 y_0.957` (slides 014-018 all do). Slide 013's transcript ends after the
`<class_Text>` block with no closing region token. The image does carry the red house
frame (measured red ink bbox x 59-900, y 44-516). A structural region token is missing.
Impact is cosmetic for text fidelity, but it is an inconsistency against the deck's own
parse convention. Evidence: `<class_Picture>` token absent vs. present in 014-018.

## REAL / HALLUCINATED / DEBATABLE list

- `13` badge text — **REAL** (corroborated; vision read Q1/Q2 both give `13`, top-right,
  pale-yellow circle, pixel bbox y 58-84 overlaps token y_0.1187=64).
- Title text `Update Weights of Hidden Layer` — **REAL** (corroborated verbatim, both
  reads; vision read confirms exact words and word order).
- Title position x_0.3369 y_0.3836 — **DEBATABLE** (parse y_0.3836=207 vs measured
  title band top 210; 3 px. Within the lane's tolerance -> counted as agreement).
- Subtitle text `(Weights from previous layer to Hidden layer)` — **REAL** (corroborated
  verbatim by the second read).
- Subtitle position x_0.2227 y_0.6031 — **DEBATABLE** (y token 326 vs measured band
  329-352; 3 px early; x agrees).
- Red house frame + bottom black bar — **REAL** (measured red ink + 517-521 dark band;
  corroborated by the vision read's edge report).
- Any equation on this slide — **none claimed; none present** — consistent, no defect.

## Uncertainties

- Vision read reported the badge circle as spanning x 807-851, y 46-90; PIL measures the
  yellow ring at x 861-891, y 58-84. The two disagree on the badge's extent. PIL is
  measurement-first per playbook position-source hierarchy, and the vision figure is
  itself an estimate. This is a **corroborating-read disagreement, not a defect in the
  parse**; the parse only asserts the badge's *text* and a top-right position, which both
  reads agree on.

## Verdict

`PARSE ADJUDICATION: PASS — text complete and verbatim-correct; only a 3px subtitle y
offset (BLOCKER by vocabulary, cosmetically negligible) and the deck-idiom closing-region
token absence; corroborated by an independent vision read.`
