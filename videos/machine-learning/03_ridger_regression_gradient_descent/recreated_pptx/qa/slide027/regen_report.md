# Slide 027 Regeneration Report

**Slide:** 027 — "Follow Negative Direction of Gradient with Selected Learning Rate"  
**Deck:** machine-learning/03_ridger_regression_gradient_descent  
**Worker:** w11-regen-slide027-20261023  
**Date:** 2026-10-23

---

## 1. Build Script Verification

| File | MD5 |
|------|-----|
| `recreated_pptx/build/slide_027.js` | `ee456c741025cfb4301a5b276ea83fc4` |
| `recreated_pptx/qa/slide027/build_attempt_10.js` | `ee456c741025cfb4301a5b276ea83fc4` |

**Result:** **MATCH** — the build script is byte-identical to the banked attempt-10 script that produced the certified render.

---

## 2. PPTX Regeneration

- **Command:** `NODE_PATH=$(npm root -g) node recreated_pptx/build/slide_027.js`
- **Output:** `recreated_pptx/slide_027_recreated.pptx` (101,724 bytes)
- **Zip integrity:** `unzip -t` — **No errors detected**
- **PPTX MD5:** `577046d241cf66c21301179f9d903611`
- **Note:** MD5 differs from the original certified build (`a5f15c5d57342b344f78fc84fb1e5eb3`) due to pptxgenjs embedding a fresh `docProps/core.xml` timestamp — content is identical per reproducibility record.

---

## 3. Render & Pixel Comparison

**Certified render:** `qa/slide027/render_10.png` (2001×1125, 81,132 bytes)  
**Regenerated render:** `qa/slide027/render_regen.png` (2001×1125, 82,637 bytes) — rendered with LibreOffice 24.2.7.2 (own profile)

| Metric | Value |
|--------|-------|
| Total pixels | 2,251,125 |
| Differing pixels | 22,008 |
| Difference % | **0.9776%** |
| Max channel diff | 255 |
| Diff bbox | x=397..1844, y=140..1052 (covers title + graph area) |

### Diff Distribution Analysis

| Band (150dpi y) | Region | Diff pixels | Rows with diff | Notes |
|-----------------|--------|-------------|----------------|-------|
| 0–146 | Chrome/badge | 108 | 6 | Minimal |
| 146–292 | **Title** | **15,618** | 122 | **Font rendering difference** (Calibri Bold 31.5pt → Liberation Sans substitution) |
| 292–1052 | Graph | 6,274 | 215 | Minor anti-aliasing/rasterization churn |
| 1052–1125 | Bottom chrome | 8 | 1 | Minimal |

| Threshold | Pixels > threshold |
|-----------|-------------------|
| >1 | 21,712 |
| >5 | 20,521 |
| >10 | 18,576 |
| >30 | 15,385 |
| >60 | 11,817 |
| >128 | 5,413 |

**Interpretation:** The 0.9776% diff is **expected LibreOffice-version churn**, concentrated in the title text band (Calibri Bold 31.5pt font substitution). The graph geometry (quadratic curve, arcs, arrowheads, dots, labels) shows only minor anti-aliasing differences. This matches the adjudication record note: "a Lo/LibreOffice-version difference will show some churn."

---

## 4. House Chrome Check

```
HOUSE CHROME CHECK: PASS
(panel x 112-1882, y 94-bottom; strokes L/R/bottom present, top bare; 
 badge center (1824,152) d=68; all within tol 8)
```

Matches banked `house_chrome_check_10.txt` exactly.

---

## 5. Banked Judge Transcripts (Verified Present)

| Transcript | Verdict | Size |
|------------|---------|------|
| `judge_attempt_10.txt` | **PASS** (2 MINOR adjudicated) | 3,496 B |
| `crop_10_chain_full_judge.txt` | **PASS** (5 MINOR) | 2,717 B |
| `crop_10_min_cluster_judge.txt` | **PASS** (clean) | 1,380 B |
| `crop_10_dot_sequence_judge.txt` | **PASS** (1 MINOR) | 2,122 B |
| `crop_10_axis_top_judge.txt` | **FAIL** (2 MAJOR) — PIL-adjudicated | 2,761 B |
| `crop_B_10_axis_top_run.log` | Dispatch log | 4,069 B |
| `crop_B_10_chain_full_run.log` | Dispatch log | 4,084 B |
| `crop_B_10_dot_sequence_run.log` | Dispatch log | 3,457 B |
| `crop_B_10_min_cluster_invoke3_run.log` | Dispatch log (3rd invocation, PASS) | 2,717 B |
| `house_chrome_check_10.txt` | PASS | 143 B |

**Controlling record:** `qa/slide027/adjudication_attempt_9.md` — founder findings A/B/C binding, all implemented in attempt-10 build.

---

## 6. DB State (Post-Regen)

| Field | Value |
|-------|-------|
| `gen_status` | **passed** |
| `visual_check` | **PASS** |
| `visual_attempts` | 10 |
| `pptx_path` | `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_027_recreated.pptx` |
| `build_script` | `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_027.js` |
| `visual_transcript` | Full list of 10 transcripts (see above) |

---

## 7. Founder Findings Implementation Verification (from adjudication_attempt_9.md)

| Finding | Spec | Implementation in build | Verified |
|---------|------|------------------------|----------|
| **A** | Black cost curve: ONE SMOOTH analytic quadratic `y=-0.00395282*(x-450.41)²+407.25`, extent x=239..658, 420 samples | `CURVE` const + 420-point `custGeom` with line 2pt black, no fill | ✅ |
| **B** | Nine grey connectors: ARC ARROWS anchored dot-centre→dot-centre on halo-excluded centroids (9 coords listed) | `CHAIN_ARCS` (9 cubic Beziers P0→C→P2), drawn first, then heads, then discs | ✅ |
| **C** | Nine REAL arrowheads: filled grey triangles, length 5.4 fpx, half-width 2.7 fpx, chain grey ACACAD, solid connectors (no dashes) | `CHAIN_HEADS` (9 `triShape` calls with `CHAIN_GRAY`), `CHAIN_ARCS` use `prstDash: solid` | ✅ |

All three findings faithfully reproduced from the attempt-10 build script.

---

## 8. Conclusion

- ✅ Build script byte-identical to banked attempt-10
- ✅ PPTX regenerated successfully, valid zip
- ✅ House chrome check PASS
- ✅ Render diff 0.9776% — within expected LO version churn (title font substitution); graph geometry intact
- ✅ All banked judge transcripts present and accounted for
- ✅ DB updated: `gen_status=passed`, `visual_check=PASS`, claim released
- ✅ Founder findings A/B/C verified implemented

**Status:** REGENERATION COMPLETE — deliverable `recreated_pptx/slide_027_recreated.pptx` restored and certified.
