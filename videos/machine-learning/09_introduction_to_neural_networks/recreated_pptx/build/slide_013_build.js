const pptxgen = require("pptxgenjs");

// Slide 013: Classification of "XOR" Truth Table
const NUM = 13;
const TITLE = 'Classification of \u201cXOR\u201d Truth Table';
const FONT = "Times New Roman";  // Serif per typography_notes

const BG = "E6E6E6";
const FRAME_RED = "C00000";  // House chrome: outer frame #C00000 (project AGENTS.md, overrides analysis)
const RED = "B22222";        // Dark red for title, table/callout borders
const BLUE = "0000FF";     // Blue for '?' weights
const BLACK = "000000";
const YELLOW = "FFD700";   // Yellow badge (default, exact hex not captured [?])
const CYAN = "CCFFFF";     // Light cyan for O/P=0
const GREEN = "CCFFCC";    // Light green for O/P=1
const PEACH = "FFF0F0";    // Peach fill for callout

const W = 13.33, H = 7.5;
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// 2. Slide-number badge - yellow circle (HOUSE CHROME LAW: x=12.48, y=0.30, 0.5x0.5,
// fill #FFF9C4, outline #FFF9C4, centered bold number 18pt #333333)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title - HOUSE CHROME LAW: text box starts y=0.28, x=0.6, w=12.13, centered
// Serif, bold, dark red #B22222
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 1.0,
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. TRUTH TABLE (middle left) - 3 columns x 5 rows with red border
// Position: middle left, x=0.5, y=1.5, w=5.0, h=2.0
// Border color per validation: #B22222 (RED) with 1pt
const tableRows = [
  [
    { text: "X\u2081", options: { bold: true, color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
    { text: "X\u2082", options: { bold: true, color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
    { text: "O/P", options: { bold: true, color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
  ],
  [
    { text: "0", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
    { text: "0", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
    { text: "0", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: CYAN } } },
  ],
  [
    { text: "0", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
    { text: "1", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
    { text: "1", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: GREEN } } },
  ],
  [
    { text: "1", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
    { text: "0", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
    { text: "1", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: GREEN } } },
  ],
  [
    { text: "1", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
    { text: "1", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: "FFFFFF" } } },
    { text: "0", options: { color: BLACK, fontFace: FONT, fontSize: 14, fill: { color: CYAN } } },
  ],
];

s.addTable(tableRows, {
  x: 0.5, y: 1.5, w: 5.0, h: 2.0,
  border: [{ type: "solid", color: RED, pt: 1 }],
  fontFace: FONT,
});

// 5. SCATTER PLOT (middle right) - GENERATED IMAGE (graphgen, 150 DPI)
// Position: middle right, x=6.0, y=1.5, w=6.0, h=3.0
// Image generated at 6.0 x 3.0 inches at 150 DPI = 900 x 450 px
s.addImage({
  path: "slide_013_xor_scatter.png",
  x: 6.0, y: 1.5, w: 6.0, h: 3.0,
});

// 6. PERCEPTRON DIAGRAM (bottom left) - GENERATED IMAGE (graphgen, 600 DPI)
// Position: bottom left, x=0.5, y=4.5, w=5.0, h=2.3
// Image generated at 5.0 x 2.3 inches at 600 DPI = 3000 x 1380 px
s.addImage({
  path: "slide_013_perceptron_diagram.png",
  x: 0.5, y: 4.5, w: 5.0, h: 2.3,
});

// 7. CALLOUT (bottom right) - "Not Linearly Separable"
// Position: bottom right, x=6.5, y=6.0, w=5.5, h=0.7
// Rounded rectangle, light peach fill #FFF0F0, red border #B22222
// Text "Not Linearly Separable" in red #B22222 ITALIC SERIF
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 6.5, y: 6.0, w: 5.5, h: 0.7,
  fill: { color: PEACH }, line: { color: RED, width: 1.5 },
});
s.addText("Not Linearly Separable", {
  x: 6.5, y: 6.0, w: 5.5, h: 0.7,
  align: "center", valign: "middle",
  fontSize: 16, italic: true, color: RED, fontFace: FONT, margin: 0,
});

// Save
const outFile = `../slide_${String(NUM).padStart(3, "0")}_recreated.pptx`;
pres.writeFile({ fileName: outFile })
  .then(() => console.log(`Saved ${outFile}`))
  .catch(err => console.error(err));