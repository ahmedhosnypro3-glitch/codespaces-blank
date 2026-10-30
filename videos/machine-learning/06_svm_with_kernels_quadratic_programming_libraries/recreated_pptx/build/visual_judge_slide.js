// visual_judge_slide.js — Visual judge for a single slide using comparison mode
// Run: node visual_judge_slide.js <slide_num>

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const SLIDE = process.argv[2];
if (!SLIDE) {
  console.error("Usage: node visual_judge_slide.js <slide_num>");
  process.exit(1);
}

const BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const ORIGINAL = path.join(BASE, "unique_slides", `slide_${SLIDE}.jpg`);
const RENDER = path.join(BASE, "qa", "slides_045_055", `slide_${SLIDE}-1.png`);
const OUT = path.join(BASE, "qa", "slides_045_055", `judge_${SLIDE}.txt`);

if (!fs.existsSync(ORIGINAL)) {
  console.error(`Original not found: ${ORIGINAL}`);
  process.exit(1);
}
if (!fs.existsSync(RENDER)) {
  console.error(`Render not found: ${RENDER}`);
  process.exit(1);
}

// Build judge prompt
const prompt = `
You are a visual judge comparing a RECREATED PPTX slide render against the ORIGINAL lecture frame.

VIEW: Slide ${SLIDE} — SVM/kernels/QP lecture frame recreation
CAPTURE: [1] Original frame (960x540, lecture slide) — file: ${ORIGINAL}
         [2] Recreated render (150dpi LibreOffice, 13.33x7.5in, 1px=1pt) — file: ${RENDER}

FACTS (measured ground truth from the ORIGINAL):
- House frame: outer red frame at x=0.15, y=0.15, w=13.03, h=7.2 (0.15in inset), border C00000 width 1.5
- Badge: yellow circle at x=12.48, y=0.30, w=0.5, h=0.5, fill FFF9C4, outline FFF9C4, centered bold numeral ${SLIDE}, color 333333, 18pt
- Title: text box at y=0.28, x=0.6, w=12.13, centered
- These are MANDATORY and override any visual difference in the original — they are the house rule
- Original frame has its own chrome (may differ from house rule); the recreation MUST use house chrome

GROUND RULES (by-design facts — these are NOT defects):
(a) House chrome intentionally overrides the original's frame/badge/title position
(b) The original may have a different background, frame, or badge style — the recreation follows house rule
(c) Any capture artifacts in the original (cursors, window chrome, black bars) are correctly omitted
(d) Typed vs handwritten rendering is at most MINOR
(e) Mandated format upgrades (Professional 2D math, generated graphs) are upgrades, not discrepancies
(f) Verdict is about fidelity of RENDERABLE CONTENT (plot, data, labels, visual elements) only

COMPARISON TASK:
Compare the CONTENT inside the house frame (plot, axes, scatter points, labels, legends, colors, layout).
Ignore: outer frame differences, badge style differences, background color differences.
Focus on: scatter plot fidelity, axis ranges, point colors/positions, decision boundaries, legends, text labels.

VERDICT: PASS or FAIL for faithful usable content match

Output format:
## 1. LAYOUT MAP
[describe both images content layout]

## 2. CONTENT FIDELITY
[compare plot area, data points, axes, labels, legends]

## 3. DEFECT LIST
[list any content discrepancies]

## 4. VERDICT
PASS / FAIL
`;

const promptFile = path.join(BASE, "qa", "slides_045_055", `judge_prompt_${SLIDE}.txt`);
fs.writeFileSync(promptFile, prompt);

// Call vision gateway for judge in comparison mode
const cmd = `python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py comparison "${ORIGINAL}" "${RENDER}" -p "${prompt}" --timeout 300 --rounds 1 --tries 1 2>&1`;

try {
  const result = execSync(cmd, { maxBuffer: 10 * 1024 * 1024, timeout: 400000 });
  fs.writeFileSync(OUT, result.toString());
  console.log(`Judge result written to ${OUT}`);
  console.log(result.toString());
} catch (e) {
  const err = e.stdout ? e.stdout.toString() : e.message;
  fs.writeFileSync(OUT, err);
  console.error(`Judge failed for slide ${SLIDE}:`, err);
  process.exit(1);
}