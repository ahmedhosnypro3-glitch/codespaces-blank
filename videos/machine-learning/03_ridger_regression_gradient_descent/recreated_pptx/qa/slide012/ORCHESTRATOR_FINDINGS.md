# Orchestrator findings for slide 012 — READ THIS FIRST

I (the orchestrator) verified your banked files directly. Verdict status:

- `crop_2_perfect_table_judge.txt` = **PASS** (table pattern; this is what 013 inherits)
- `judge_attempt_2.txt` (full-slide, Template A) = **FAIL**

## FAIL findings requiring a fix (verbatim from judge_attempt_2.txt)

1. **MAJOR (high confidence) — outlier labels are NOT verbatim.**
   Original (BOTH lower tables): **"X5  is Outlier" / "X5 is Outlier"** — capital X, digit **5**.
   Your recreation (both lower tables): **"x8 is Outlier"** — lowercase x, digit **8**.
   You appear to have "corrected" the original's label to match the X8 highlight column.
   **Fidelity requires the original's VERBATIM text. Measure the original at native
   resolution to confirm, then restore "X5 is Outlier" in both lower tables.**
   This is a semantic content change (which variable is the outlier), not styling.

2. **MINOR (medium)** — "Test Data" label: original is an unfilled text label
   (green/blue ink, no solid box); you used a solid blue rectangle with white text.

3. **MINOR (medium)** — test-table colours: original's y-row values (60, 80, 100) are
   **red** and Test1–Test3 headers are **greenish**; you render everything blue.
   Numeric data itself matches.

4. **MINOR (low)** — table cells carry a faint green-gray tint; original reads white/very light.

5. **MINOR (low)** — arrow anchor: original stems near the X6/X7 header area of the
   second table; you stem from the table's right edge.

## Verified matching — do NOT touch
Title verbatim red bold; badge "12"; "Training Data", "Perfect Data / Y follows x1";
all three data tables with every cell value including the 1/2/3/4/8/9/10/11 and
1/3/5/6/16/7/5/3 and y rows; yellow highlight on X8-column values 30 and 60;
Test Data table values; "Again / Y follows x1" red box; question-box text;
no overflow/clipping/collisions; cells vertically centered.

## Downstream obligation (13 → 17 → 18 chain)
Your table PATTERN is inherited by slide 013. Keep the table COMPONENT structure intact
and ensure it is exported in `recreated_pptx/build/components/slide_012.js`
(renderBase + per-block exports) so 013 can `require` it. 013 redraws at its OWN measured
position/numbers, so the fixes above are exactly what 013 must inherit.

## After fixing
Re-render to a NEW numbered render, run house_chrome_check.py (must pass), re-judge BOTH
legs, then record-visual 12 PASS + set gen_status passed + release.
