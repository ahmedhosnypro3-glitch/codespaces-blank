// Build script for slide 007 of
// videos/machine-learning/03_ridger_regression_gradient_descent
// "Problems of Linear Regression"
//
// Frame geometric measurements (unique_slides/slide_007.jpg, 960x540 px = slide pts,
// taken on 2026-10-23 by the worker, PIL-based):
//   title red ink            x 242..677, y 78..100   -> centered, 30pt bold Arial #C00000
//   blue content box         outer x 78..885, y 120..513; stroke cores x 80.5 / 881.5,
//                            y 122.5 / 510; fill FFFFFF, border 2px #0000FF
//   body text lines (ink tops / rgb size):
//     1 intro                y 154, x 90..809   ~18pt  (dark red #A00A24 JPEG, nominal #C00000)
//     2 header               y 202, x 90..562   ~20pt  (#0000FF bold)
//     3 bullet1              y 249, x 92..562   ~22pt  (#0000FF bold)
//     4 bullet2              y 294, x 92..554   ~22pt  (#0000FF bold + #C00000 italic paren)
//     5 bullet3              y 348, x 92..630   ~22pt  (#0000FF bold + #C00000 italic paren)
//     6 bullet4              y 397, x 92..858   ~22pt  (#0000FF bold + #C00000 italic paren)
//   inter-line pitch (ink-top to ink-top): 48, 47, 45, 54, 49 -> pinned 48pt pitch with a
//   one-off 6pt widening before the two long bullets (measured 54 = 48 + 6).
//
// Spec-derived facts NOT visible in the JPEG (analysis/slide_007_final.json, verbatim law):
//   - intro line's underlined key phrases "linearly separable" and "Linear regression model"
//   - section header is underlined (recreation_brief step 6)
//   - the ➢ (U+27A2) bullet glyph is per spec; the JPEG's bullet glyph is a different
//     check-mark-like char that the matplotlib target glyph cannot reproduce.
// Every glyph, color and coordinate above comes from the frame; the §-items are spec text.
// VERBATIM text is preserved exactly, including "[1]" / "[2]" and "FOUR" in caps.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.join(
  __dirname, "..", "..", "shared_patterns", "house_chrome.js"
));

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const FONT = "Arial";
const BLUE = "0000FF";
const RED = "C00000";
const INTRO_RED = "C00000";

const slide = pptx.addSlide();

// House chrome: white canvas + E9E9E7 panel + C00000 left/right/bottom strokes (NO top
// stroke) + FDFD96 badge with purple ring, numeral 7.
drawHouseChrome(pptx, slide, { numeral: 7 });

// ---- Title: "Problems of Linear Regression" -----------------------------------
// Frame: red ink x 242..677 (w 435, center 459.5) y 78..100. Centered on the slide,
// top band. 30pt caps height ~= 20px ~= 1pt/1.5px -> 30pt.
slide.addText("Problems of Linear Regression", {
  x: 0, y: 1.028,
  w: 13.333, h: 0.62,
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: FONT,
  margin: 0,
});

// ---- Blue content box ---------------------------------------------------------
// Frame: outer x 78..885, y 120..513 (w 807 x h 393). Fill FFFFFF, border 0000FF.
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 78 / 72, y: 120 / 72, w: 807 / 72, h: 393 / 72,
  fill: { color: "FFFFFF" }, line: { color: BLUE, width: 2 },
});

// ---- Body text ----------------------------------------------------------------
// Left column of the box; x 88 (frame) -> 88/72 in; box width available 807/72 - margins.
const BX = 88 / 72;
const BW = 790 / 72;

// Line 1 — intro: "Assume the Dataset is linearly separable (suitable to apply
// Linear regression model)". Dark-red / maroon, 18pt, smallest body text per spec.
// FRAME-vs-SPEC: spec (5) claims underlined key phrases [?], but PIL on the original
// (unique_slides/slide_007.jpg) shows NO underline on this line — rows y173..175 carry
// only ~90 px of ink (descender tails), vs 472 px on the header's y220-221 underline
// stroke. Frame wins: the intro line is drawn WITHOUT underlines.
slide.addText(
  [
    { text: "Assume the Dataset is ", options: { color: INTRO_RED, fontSize: 18 } },
    { text: "linearly separable", options: { color: INTRO_RED, fontSize: 18 } },
    { text: " (suitable to apply ", options: { color: INTRO_RED, fontSize: 18 } },
    { text: "Linear regression model", options: { color: INTRO_RED, fontSize: 18 } },
    { text: ")", options: { color: INTRO_RED, fontSize: 18 } },
  ],
  {
    x: BX, y: 146 / 72, w: BW, h: 40 / 72,
    fontSize: 18, color: INTRO_RED, fontFace: FONT,
    lineSpacing: 22, margin: 0, valign: "top",
  }
);

// Line 2 — section header: "Linear regression model has FOUR problems:",
// blue bold, underlined, 20pt.
slide.addText("Linear regression model has FOUR problems:", {
  x: BX, y: 194 / 72, w: BW, h: 44 / 72,
  fontSize: 20, bold: true, color: BLUE, fontFace: FONT,
  underline: true, margin: 0, valign: "top",
});

// Line 3 — bullet 1: "➢Overfitting Problem" — blue bold, 22pt.
slide.addText("\u27A2Overfitting Problem", {
  x: BX, y: 241 / 72, w: BW, h: 44 / 72,
  fontSize: 22, bold: true, color: BLUE, fontFace: FONT,
  margin: 0, valign: "top",
});

// Line 4 — bullet 2: "➢Matrix Inversion Problem [1] (Singular Matrix)".
// Main phrase blue bold; the parenthetical is red italic (spec).
slide.addText(
  [
    { text: "\u27A2Matrix Inversion Problem [1] ", options: { color: BLUE, bold: true } },
    { text: "(Singular Matrix)", options: { color: RED, italic: true, bold: true } },
  ],
  {
    x: BX, y: 286 / 72, w: BW, h: 44 / 72,
    fontSize: 22, fontFace: FONT, margin: 0, valign: "top",
  }
);

// Line 5 — bullet 3: "➢Matrix Inversion Problem [2] (Large Matrix dimension)".
slide.addText(
  [
    { text: "\u27A2Matrix Inversion Problem [2] ", options: { color: BLUE, bold: true } },
    { text: "(Large Matrix dimension)", options: { color: RED, italic: true, bold: true } },
  ],
  {
    x: BX, y: 340 / 72, w: BW, h: 44 / 72,
    fontSize: 22, fontFace: FONT, margin: 0, valign: "top",
  }
);

// Line 6 — bullet 4: "➢Different Hyperplanes can solve the problems (Selection of Best
// Hyperplane)". FRAME-MEASURED: this is the longest line (orig x92..859 = 768pt) and at
// 22pt it wrapped to a second line in LO (rendered 810.8pt > 792pt usable). Compressed
// with negative charSpacing so it fits one line at the same font size as the other
// bullets (never font size — that breaks cap-height/baseline metrics).
// residual (measured at -0.3pt) = 801 - 790 = 11pt over 76 glyph gaps -> charSpacing -0.6pt.
slide.addText(
  [
    { text: "\u27A2Different Hyperplanes can solve the problems ", options: { color: BLUE, bold: true } },
    { text: "(Selection of Best Hyperplane)", options: { color: RED, italic: true, bold: true } },
  ],
  {
    x: BX, y: 389 / 72, w: BW, h: 44 / 72,
    fontSize: 22, fontFace: FONT, margin: 0, valign: "top", charSpacing: -0.6,
  }
);

const OUT = path.resolve(
  __dirname, "..", "..", "recreated_pptx", "slide_007_recreated.pptx"
);
pptx.writeFile({ fileName: OUT }).then(() => console.log("done", OUT));
