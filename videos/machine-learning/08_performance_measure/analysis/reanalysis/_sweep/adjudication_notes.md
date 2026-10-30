# Adjudication notes — slides 1-13 re-analysis sweep

Method: first read = analysis/slide_NNN_final.json when it exists, else analysis/slide_NNN_raw.json
(unvalidated). Reanalysis = analysis/reanalysis/slide_NNN_raw.json (independent vision read,
finish=stop). Third read = banked doc-parse crop-cascade under pool_run/docparse/slideNNN/.
Materiality rule: a string the build would visibly miss, a differing data value, or a missing
visual element. Cosmetic rewording / field-bucket moves are NOT drift.

## 001 — first: final | re: finish=stop
- Title identical.
- Buckets differ (first put attribution lines in labels, re in bullets) — cosmetic, all strings present.
- MATERIAL: label "OF SCIENCE AND TECHNOLOGY" present in first read (and drawn by build/slide_001.js),
  ABSENT in reanalysis labels. Pending targeted zoom verification.
- MATERIAL (pending): Arabic logo line first "جامعة زويل للعلوم والتكنولوجيا" vs re
  "جامعة العلوم والتكنولوجيا" (re drops "زويل"). Build draws the first-read string as native text
  (slide_001.js:119), so a reanalysis-driven rebuild would print a wrong Arabic string.
- Reanalysis ADDS: none material. Course code "CSAI 253 - Spring 2024" present in both
  (first via visual_elements V5, re via layout regions + recreation_brief step 3).

## 002 — first: final | re: finish=stop
- Title identical. All flowchart strings present in both.
- NOT drift: first read lists the ten label entries as bullets (+1 x5, 0 x5); re lists "+1"/"0"
  once in labels BUT its visual element states "a narrow label strip ... shows +1 five times" and
  "shows 0 five times" — repetition is captured, build-safe.
- NOT drift: "Label of Input Sample (+1, 0)" — re splits into two labels ("Label of Input Sample",
  "(+1, 0)"), content intact.
- MINOR: "[Any value] -> (-1, +1)" (first, also in docparse for slide 3 as "[Any value]") vs
  "(Any value) → (-1, +1)" (re) — square brackets vs parentheses, ASCII arrow vs U+2192.
- MINOR (first-read gap): reanalysis resolves the sigmoid axes (0 at bottom, 1 at top) and names the
  0.5 threshold; first read V3 only says "axes visible".

## 003 — first: final | re: finish=stop
- Title identical. +1 x5 / -1 x5 preserved in re labels (and in its visual description).
- NOT drift: first read merges "Positive Class “Shoot the Enemy”" into one label; re splits into
  "Positive Class" + "\"Shoot the Enemy\"" — all strings present.
- NOT drift: re has NO equations array; the ranges live in labels ("(Any value) → (-1, +1)",
  "(+1, -1)"). FLAG (formatting only, not content): a build worker consuming ONLY reanalysis may
  render these ranges as plain text instead of professional 2D math.

## 004 — first: raw only (no final yet) | re: finish=stop
- Title identical. All six numbers (30, 70, 18, 12, 10, 60) and every row/column label present in
  re's visual_elements even though re omits them from the labels array — NOT drift.
- MINOR (color only, outside the compared field list): first read says FN/FP cells "on white";
  reanalysis says FN/FP "with yellow fill". Slide 4 has no build script yet, so this is actionable
  for its build worker.
