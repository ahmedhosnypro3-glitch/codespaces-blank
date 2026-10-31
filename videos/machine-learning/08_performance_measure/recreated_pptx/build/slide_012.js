// slide_012 — "Recall" — 08_performance_measure — v2 (judge attempt 5 FAIL fixes)
// Frame-measured build (960x540 px, 1px = 1pt = 1/72 in). Measurements: scratch/s12/measure*.py
const pptxgenpkg = require("pptxgenjs");
const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const FONT = "Arial";
const A = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";

let s = pptx.addSlide();
s.background = { color: BG };

// House chrome (root AGENTS.md 2026-10-09 — overrides everything)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("12", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
s.addText("Recall", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.75, align: "center", valign: "middle",
  fontSize: 40, bold: true, color: "B00000", fontFace: FONT, margin: 0,
});

// Definition box (gray, red divider): orig x70-656 y101-209, divider y148-150 x81-645
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.97, y: 1.40, w: 8.14, h: 1.50,
  fill: { color: "C0C0C0" }, line: { color: "C0C0C0", width: 0.75 },
});
s.addShape(pptx.shapes.LINE, {
  x: 1.13, y: 2.056, w: 7.83, h: 0,
  line: { color: RED, width: 2.25 },
});
s.addText("Correctly Classified (as Positive)", {
  x: 0.97, y: 1.44, w: 8.14, h: 0.60, align: "center", valign: "middle",
  fontSize: 16, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText("Total objects that should be retrieved (Actually Positive)", {
  x: 0.97, y: 2.10, w: 8.14, h: 0.72, align: "center", valign: "middle",
  fontSize: 16, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});

// Meaning panel (pale yellow) + header + question: orig panel y~200-260 x75-546
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.04, y: 2.78, w: 6.40, h: 0.88,
  fill: { color: "F7FBD6" }, line: { color: "F7FBD6", width: 0.5 },
});
s.addText("Meaning", {
  x: 1.04, y: 2.82, w: 2.5, h: 0.42,
  fontSize: 20, bold: true, color: "B00000", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "Does the classified ", options: { fontSize: 15, color: TEXT, fontFace: FONT } },
  { text: "miss", options: { fontSize: 15, color: RED, underline: true, fontFace: FONT } },
  { text: " any of ", options: { fontSize: 15, color: TEXT, fontFace: FONT } },
  { text: "Positive", options: { fontSize: 15, color: "0000CC", underline: true, fontFace: FONT } },
  { text: " Objects ?", options: { fontSize: 15, color: TEXT, fontFace: FONT } },
], {
  x: 1.06, y: 3.22, w: 7.6, h: 0.40, margin: 0, valign: "middle",
});

// Formula box: red rounded rect orig x70-303 y263-321
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.97, y: 3.65, w: 3.24, h: 0.81,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2 }, round: 0.15,
});
s.addText("Recall =", {
  x: 1.14, y: 3.90, w: 1.35, h: 0.40, valign: "middle",
  fontSize: 18, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});
s.addImage({ path: A + "/eq_012_frac.png", x: 3.05, y: 3.68, w: 1.27, h: 0.59667 });

// Precision callout with thin border: orig text x340-500 y294-332
s.addShape(pptx.shapes.RECTANGLE, {
  x: 4.72, y: 4.02, w: 2.30, h: 0.68,
  fill: { color: "FFFFFF" }, line: { color: "A6A6A6", width: 0.75 },
});
s.addText("Precision=", {
  x: 4.80, y: 4.08, w: 1.38, h: 0.30, valign: "middle",
  fontSize: 15, color: TEXT, fontFace: FONT, margin: 0,
});
s.addImage({ path: A + "/eq_012_prec.png", x: 6.20, y: 4.10, w: 0.51333, h: 0.30167 });
s.addText("=100%", {
  x: 4.80, y: 4.40, w: 1.20, h: 0.28, valign: "middle",
  fontSize: 15, color: TEXT, fontFace: FONT, margin: 0,
});

// Speech bubbles: orig left x105-215 y340-380, right x220-325 y340-380
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 1.46, y: 4.72, w: 1.53, h: 0.56,
  fill: { color: "FFF2CC" }, line: { color: "D0D0D0", width: 1 }, round: 0.12,
});
s.addText("Positive", {
  x: 1.46, y: 4.76, w: 1.53, h: 0.24, align: "center",
  fontSize: 10.5, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText("Classified as +ive", {
  x: 1.46, y: 5.00, w: 1.53, h: 0.24, align: "center",
  fontSize: 10.5, color: TEXT, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 3.06, y: 4.72, w: 1.46, h: 0.56,
  fill: { color: "FFF2CC" }, line: { color: "D0D0D0", width: 1 }, round: 0.12,
});
s.addText("Positive", {
  x: 3.06, y: 4.76, w: 1.46, h: 0.24, align: "center",
  fontSize: 10.5, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText("Classified as -ive", {
  x: 3.06, y: 5.00, w: 1.46, h: 0.24, align: "center",
  fontSize: 10.5, color: TEXT, fontFace: FONT, margin: 0,
});
// Pointer lines from formula box down to each bubble
s.addShape(pptx.shapes.LINE, { x: 3.30, y: 4.46, w: -1.10, h: 0.26, line: { color: "808080", width: 1 } });
s.addShape(pptx.shapes.LINE, { x: 3.50, y: 4.46, w: 0.30, h: 0.26, line: { color: "808080", width: 1 } });

// Green brace (cropped from original, white keyed transparent): orig x98-346 y380-408
s.addImage({ path: A + "/brace_012.png", x: 1.36, y: 5.28, w: 3.44444, h: 0.38889 });
s.addText("All Positive Samples in the Dataset", {
  x: 1.22, y: 5.61, w: 3.42, h: 0.30, valign: "middle",
  fontSize: 13, italic: true, underline: true, color: "8B3A3A", fontFace: FONT, margin: 0,
});

// Model box: orig blue-bordered x60-500 y437-505
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.83, y: 6.07, w: 6.11, h: 0.94,
  fill: { color: "FFFFFF" }, line: { color: "4472C4", width: 1.5 },
});
s.addText("Model Try to catch ALL Positive Samples", {
  x: 0.94, y: 6.14, w: 5.8, h: 0.32, valign: "middle",
  fontSize: 14, bold: true, italic: true, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "(Irrespective of classifying ", options: { fontSize: 13, italic: true, color: TEXT, fontFace: FONT } },
  { text: "NEGATIVE", options: { fontSize: 13, italic: true, bold: true, color: RED, fontFace: FONT } },
  { text: " Objects as Positive)", options: { fontSize: 13, italic: true, color: TEXT, fontFace: FONT } },
], {
  x: 0.94, y: 6.50, w: 5.9, h: 0.32, valign: "middle", margin: 0,
});

// ---- Right column: confusion matrices (orig x674-865; m1 y53-165, m2 y168-288) ----
function matrix(x, y, rowH, cells) {
  const w = 2.66;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: y, w: w, h: rowH.reduce((a, b) => a + b, 0),
    fill: { color: "FFFFFF" }, line: { color: "4472C4", width: 2 },
  });
  const hdr = { fontSize: 11, bold: true, color: RED, fill: { color: "EDF0F8" }, align: "center", valign: "middle" };
  const lab = { fontSize: 11, bold: true, color: TEXT, fill: { color: "EDF0F8" }, align: "center", valign: "middle" };
  const data = [
    [{ text: "", options: { fill: { color: "EDF0F8" } } },
     { text: "Predicted as", options: { ...hdr, colspan: 2 } }],
    [{ text: "", options: { fill: { color: "EDF0F8" } } },
     { text: "P", options: lab }, { text: "N", options: lab }],
    [{ text: "P", options: lab }, cells[0][0], cells[0][1]],
    [{ text: "N", options: lab }, cells[1][0], cells[1][1]],
  ];
  s.addTable(data, {
    x: x, y: y, w: w, colW: [0.66, 1.0, 1.0], rowH: rowH,
    fontFace: FONT, color: TEXT,
    border: [{ type: "solid", color: "4472C4", width: 0.75 }],
  });
  // Vertical "Actual" label in the corner column, spanning the two data rows
  const cy = y + rowH[0] + rowH[1] + (rowH[2] + rowH[3]) / 2;
  s.addText("Actual", {
    x: x + 0.33 - 0.14, y: cy - 0.50, w: 0.28, h: 1.0,
    rotate: 270, align: "center", valign: "middle",
    fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
}
const cell = (t, fill) => ({
  text: t, options: { fontSize: 13, bold: true, color: TEXT, fill: { color: fill }, align: "center", valign: "middle" },
});
// Matrix 1 (top): TP green, FN pink, FP pink, TN green
matrix(9.36, 0.74, [0.36, 0.32, 0.44, 0.43], [
  [cell("TP", "84FC00"), cell("FN", "FFCCCC")],
  [cell("FP", "FFCCCC"), cell("TN", "84FC00")],
]);
// Matrix 2 (below): 30 (blue-circled) white, FN 0 peach, FP 70 white, TN 0 green
matrix(9.36, 2.33, [0.36, 0.32, 0.50, 0.49], [
  [cell("30", "FFFFFF"), cell("0", "EFCCA8")],
  [cell("70", "FFFFFF"), cell("0", "84FC00")],
]);
// Blue circle around the "30" cell (m2 row P, col P): center (10.52, 3.26)
s.addShape(pptx.shapes.OVAL, {
  x: 10.29, y: 3.03, w: 0.46, h: 0.46,
  line: { color: "0000FF", width: 2 },
});

// ---- Bottom-right decision trees inside red panel (orig panel x536-881 y~295-503) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.44, y: 4.10, w: 4.79, h: 2.89,
  line: { color: RED, width: 1.5 },
});
s.addText("Positive", {
  x: 7.40, y: 4.14, w: 1.90, h: 0.26, align: "center",
  fontSize: 15, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Negative", {
  x: 10.40, y: 4.14, w: 1.90, h: 0.26, align: "center",
  fontSize: 15, bold: true, color: "00B050", fontFace: FONT, margin: 0,
});
// Airplane icons (cropped from original frame)
s.addImage({ path: A + "/icon_012_left.png", x: 7.57, y: 4.40, w: 2.09722, h: 1.19444 });
s.addImage({ path: A + "/icon_012_right.png", x: 10.58, y: 4.40, w: 1.44444, h: 1.19444 });
// Panels behind trees
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.72, y: 5.25, w: 1.61, h: 1.57, fill: { color: "F5F0A0" }, line: { color: "F5F0A0", width: 0.5 },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 10.25, y: 5.25, w: 1.78, h: 1.57, fill: { color: "FFFFFF" }, line: { color: "D0D0D0", width: 0.5 },
});
// Connectors
function link(x1, y1, x2, y2) {
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  s.addShape(pptx.shapes.LINE, {
    x: x, y: y, w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
    flipV: y2 < y1, flipH: x2 < x1,
    line: { color: TEXT, width: 1.25 },
  });
}
link(8.60, 5.55, 7.96, 6.38);
link(8.60, 5.55, 9.18, 6.40);
link(11.11, 5.52, 10.47, 6.40);
link(11.11, 5.52, 11.74, 6.38);
function node(cx, cy, fill, label, val) {
  const d = 0.42;
  s.addShape(pptx.shapes.OVAL, {
    x: cx - d / 2, y: cy - d / 2, w: d, h: d,
    fill: { color: fill }, line: { color: fill, width: 1 },
  });
  s.addText(val, {
    x: cx - d / 2, y: cy - d / 2, w: d, h: d, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
  if (label) {
    s.addText(label, {
      x: cx - 0.3, y: cy + d / 2 + 0.02, w: 0.6, h: 0.25, align: "center",
      fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0,
    });
  }
}
node(8.60, 5.55, "C86408", "", "30");       // Positive root
node(7.96, 6.38, "C86408", "TP", "30");     // TP
node(9.18, 6.40, "6EB728", "FN", "0");      // FN
node(11.11, 5.52, "08823A", "", "70");      // Negative root
node(10.47, 6.40, "08823A", "TN", "0");     // TN
node(11.74, 6.38, "9C0000", "FP", "70");    // FP
// Small red dot beside the Negative root "70"
s.addShape(pptx.shapes.OVAL, {
  x: 11.62, y: 5.46, w: 0.12, h: 0.12,
  fill: { color: "9C0000" }, line: { color: "9C0000", width: 0.5 },
});

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_012_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done"));
