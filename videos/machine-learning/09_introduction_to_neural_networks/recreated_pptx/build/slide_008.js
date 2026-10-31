// Pattern: house-chrome + slide 008 content (Multi-Class One-vs-All classification)
// Build: NODE_PATH=$(npm root -g) node slide_008.js
//
// Geometry measured from unique_slides/slide_008.jpg (960x540, 1px == 1pt).
// Inner white plot panel: x 167-798, y 120-505 (drawn as the graph image).
const pptxgen = require("pptxgenjs");

const NUM = 8;
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };  // house template background

// ===== HOUSE CHROME (non-negotiable) =====

// 1. outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. slide-number badge (yellow oval + centered bold numeral) - numeral = printed number (8)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. title - TWO lines, matching the original's measured line breaks
//    line 1 red "Multi-Class Classification using"
//    line 2 pure-blue "[ONE VS ALL]" + red " Binary Classifiers"
s.addText([
  { text: "Multi-Class Classification using", options: { breakLine: true, color: "CC2222", bold: true, fontSize: 24, fontFace: FONT } },
  { text: "[ONE VS ALL]", options: { color: "0000FF", bold: true, fontSize: 24, fontFace: FONT } },
  { text: " Binary Classifiers", options: { color: "CC2222", bold: true, fontSize: 24, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.85,
  align: "center", valign: "top", margin: 0,
});

// 4. bottom black bar (video player overlay; measured rows 518-539)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.0, y: 7.19, w: W, h: 0.31,
  fill: { color: "000000" },
  line: { type: "none" },
});

// ===== SLIDE 008 CONTENT =====
// Conversion: 960x540 original px -> 13.33x7.5 in. 1px = 1pt = 1/72in.
// The graph PNG is generated on the original pixel grid (632 x 386 px = inner
// panel), so it is embedded at exact size (no rescale).

// Plot panel measured x 167-798, y 120-505 px
const PX0 = 167 / 72, PY0 = 120 / 72, PW = 632 / 72, PH = 386 / 72;

// 5. white panel ground under the image
s.addShape(pres.shapes.RECTANGLE, {
  x: PX0, y: PY0, w: PW, h: PH,
  fill: { color: "FFFFFF" },
  line: { type: "none" },
});

// 6. the advanced graph: hatched class regions (green / lavender / pink / grey),
//    red axes with red arrowheads, three decision boundaries, ticks, clusters.
s.addImage({
  path: "slide_008_graph_v2.png",
  x: PX0, y: PY0, w: PW, h: PH,
});

// ===== Annotations (native shapes/text, positioned in original px) =====
const inx = (px) => px / 72;
const iny = (py) => py / 72;

function callout(px, py, w, h, text, fill, line, textColor, fontSize) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: inx(px), y: iny(py), w: inx(w), h: iny(h),
    fill: { color: fill }, line: line ? { color: line, width: 1 } : { type: "none" },
  });
  s.addText(text, {
    x: inx(px), y: iny(py), w: inx(w), h: iny(h),
    align: "center", valign: "middle",
    fontSize: fontSize, bold: true, color: textColor, fontFace: FONT, margin: 0,
  });
}

// --- Class tag boxes: bright yellow #ffff00, black text (measured px) ---
callout(525, 153, 34, 29, "C1", "FFFF00", null, "000000", 14);
callout(594, 295, 34, 29, "C2", "FFFF00", null, "000000", 14);
callout(260, 395, 34, 29, "C3", "FFFF00", null, "000000", 14);

// --- "?" boxes: pale-pink #ffe0cc fill, red-orange #ff3300 "?" (measured px) ---
const qBoxes = [
  [434, 318, 43, 35],
  [591, 177, 41, 32],
  [243, 264, 39, 32],
  [422, 418, 39, 33],
];
for (const [qx, qy, qw, qh] of qBoxes) {
  callout(qx, qy, qw, qh, "?", "FFE0CC", null, "FF3300", 16);
}

// --- "+ve" labels: black text (measured px) ---
const pve = [[638, 131], [251, 312], [494, 448]];
for (const [px, py] of pve) {
  s.addText("+ve", {
    x: inx(px), y: iny(py), w: inx(40), h: iny(16),
    align: "left", valign: "top",
    fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
}

// --- Decision-boundary labels (rotated along each line, measured px centers) ---
function dLabel(cx, cy, text, color, rotate) {
  s.addText(text, {
    x: inx(cx - 18), y: iny(cy - 11), w: inx(36), h: inx(22),
    align: "center", valign: "middle",
    rotate: rotate,
    fontSize: 12, bold: true, color: color, fontFace: FONT, margin: 0,
  });
}
dLabel(272, 194, "d1(x)", "CC2222", 35);    // red, upper-left diagonal
dLabel(576, 154, "d2(x)", "0000FF", -40);   // blue, steep diagonal
dLabel(725, 212, "d3(x)", "00A000", -15);   // green, right end

// --- "Undefined" callout: WHITE fill, BLUE border + text + BLUE leaders ---
// Measured box x 73-147, y 131-160 - in the gap between the outer house frame
// (x 59) and the inner plot panel (x 167), i.e. outside the panel.
const undefX = inx(73), undefY = iny(131), undefW = inx(74), undefH = iny(29);
s.addShape(pres.shapes.RECTANGLE, {
  x: undefX, y: undefY, w: undefW, h: undefH,
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 },
});
s.addText("Undefined", {
  x: undefX, y: undefY, w: undefW, h: undefH,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
});

// Two thin BLUE leader lines from the box's right edge into the plot.
s.addShape(pres.shapes.LINE, {
  x: inx(138), y: iny(140), w: inx(62), h: iny(12),
  line: { color: "0000FF", width: 0.75 },
});
s.addShape(pres.shapes.LINE, {
  x: inx(138), y: iny(152), w: inx(105), h: iny(12),
  line: { color: "0000FF", width: 0.75 },
});

// --- "New Class" box: WHITE fill, MAGENTA border + text (measured px) ---
const ncX = inx(715), ncY = iny(372), ncW = inx(71), ncH = iny(23);
s.addShape(pres.shapes.RECTANGLE, {
  x: ncX, y: ncY, w: ncW, h: ncH,
  fill: { color: "FFFFFF" }, line: { color: "FF00FF", width: 1 },
});
s.addText("New Class", {
  x: ncX, y: ncY, w: ncW, h: ncH,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "FF00FF", fontFace: FONT, margin: 0,
});

pres.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_008_recreated.pptx"
}).then(() => console.log("wrote slide_008_recreated.pptx"));
