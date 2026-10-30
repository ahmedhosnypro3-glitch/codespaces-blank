// Build slide 030: Example - Bad Weights (badge 30)
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";

// ---- HOUSE CHROME ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFD966" }, line: { color: "000000", width: 1.5 },
});
s.addText("30", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// Title "Example" in red serif
s.addText("Example", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "left", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: "Times New Roman", margin: 0,
});

// "Bad Weights" in pink box below title
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 0.85, w: 2.5, h: 0.35,
  fill: { color: "F8CBAD" }, line: { color: "F8CBAD", width: 0 },
});
s.addText("Bad Weights", {
  x: 0.6, y: 0.85, w: 2.5, h: 0.35,
  align: "center", valign: "middle",
  fontSize: 12, color: "000000", fontFace: FONT, margin: 0,
});

// Neural network diagram with red border
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.5, y: 0.5, w: 9.0, h: 3.5,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 2 },
});

// Input vector labels x1, x2
s.addText("x1", { x: 3.7, y: 1.2, w: 0.5, h: 0.3, align: "right", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
s.addText("x2", { x: 3.7, y: 1.8, w: 0.5, h: 0.3, align: "right", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });

// Input values [7], [4] in bracket
s.addShape(pres.shapes.RECTANGLE, {
  x: 4.3, y: 1.0, w: 0.5, h: 1.0,
  fill: { type: "none" }, line: { color: "000000", width: 1 },
});
s.addText("[7]\n[4]", { x: 4.3, y: 1.0, w: 0.5, h: 1.0, align: "center", valign: "middle", fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0 });

// Hidden layer weights from inputs
// Weights from x1: 0.1, 0.2, 0.3
// Weights from x2: 0.4, 0.5, 0.6
s.addText("0.1  0.2  0.3", { x: 4.9, y: 0.9, w: 1.5, h: 0.3, align: "left", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });
s.addText("0.4  0.5  0.6", { x: 4.9, y: 1.6, w: 1.5, h: 0.3, align: "left", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });

// Hidden nodes 3, 4, 5 (yellow circles)
for (let i = 0; i < 3; i++) {
  const y = 1.0 + i * 0.5;
  s.addShape(pres.shapes.OVAL, {
    x: 6.5, y: y, w: 0.5, h: 0.5,
    fill: { color: "FFE699" }, line: { color: "000000", width: 1 },
  });
  s.addText([3, 4, 5][i].toString(), {
    x: 6.5, y: y, w: 0.5, h: 0.5,
    align: "center", valign: "middle", fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
  s.addText(["O3", "O4", "O5"][i], {
    x: 6.5, y: y - 0.3, w: 0.5, h: 0.3,
    align: "center", fontSize: 10, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
  });
}

// Output nodes 6, 7 (orange circles)
for (let i = 0; i < 2; i++) {
  const y = 1.25 + i * 1.0;
  s.addShape(pres.shapes.OVAL, {
    x: 8.5, y: y, w: 0.5, h: 0.5,
    fill: { color: "F4B183" }, line: { color: "000000", width: 1 },
  });
  s.addText([6, 7][i].toString(), {
    x: 8.5, y: y, w: 0.5, h: 0.5,
    align: "center", valign: "middle", fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
  s.addText(["O6", "O7"][i], {
    x: 9.0, y: y + 0.1, w: 0.5, h: 0.3,
    align: "left", fontSize: 10, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
  });
}

// Weights from hidden to output: 0.3, 0.4, 0.5 (red)
s.addText("0.3  0.4  0.5", { x: 7.2, y: 1.0, w: 1.0, h: 0.3, align: "center", fontSize: 10, bold: true, color: "FF0000", fontFace: FONT, margin: 0 });

// Output / Target labels
s.addText("Output", { x: 9.5, y: 0.8, w: 1.0, h: 0.3, align: "center", fontSize: 11, bold: true, color: "000000", fontFace: FONT, margin: 0 });
s.addText("Target", { x: 10.5, y: 0.8, w: 1.0, h: 0.3, align: "center", fontSize: 11, bold: true, color: "000000", fontFace: FONT, margin: 0 });

// Target column [0] t6 / [1] t7
s.addText("[0]  t6", { x: 9.5, y: 1.2, w: 1.0, h: 0.5, align: "center", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
s.addText("[1]  t7", { x: 9.5, y: 1.8, w: 1.0, h: 0.5, align: "center", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });

// Dashed lines from output to target
for (let i = 0; i < 2; i++) {
  const y = 1.5 + i * 1.0;
  s.addShape(pres.shapes.LINE, {
    x: 9.0, y: y, w: 0.5, h: 0,
    line: { color: "000000", width: 1, dashType: "dash", endArrow: "triangle" },
  });
}

// "Forward" label in blue italic
s.addText("Forward", { x: 0.6, y: 4.2, w: 1.5, h: 0.3, align: "left", fontSize: 14, bold: true, italic: true, color: "0000FF", fontFace: "Times New Roman", margin: 0 });

// Blue equation boxes (Net calculations)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.6, w: 4.0, h: 1.2,
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 },
});
s.addText(
  "Net3 = 7 * 0.1 + 4 * 0.4 = 2.3\nNet4 = 7 * 0.2 + 4 * 0.5 = 3.4\nNet5 = 7 * 0.3 + 4 * 0.6 = 4.5",
  { x: 0.6, y: 4.6, w: 3.8, h: 1.2, fontSize: 11, color: "000000", fontFace: FONT, margin: 0.1 }
);
// Make Net3, Net4, Net5 red
s.addText("Net3", { x: 0.6, y: 4.6, w: 0.8, h: 0.3, fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("Net4", { x: 0.6, y: 4.9, w: 0.8, h: 0.3, fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("Net5", { x: 0.6, y: 5.2, w: 0.8, h: 0.3, fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 5.9, w: 6.5, h: 0.8,
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 },
});
s.addText(
  "Net6 = 0.909 * 0.3 + 0.968 * 0.4 + 0.989 * 0.5 = 1.1544\nNet7 = 0.909 * 0.3 + 0.968 * 0.4 + 0.989 * 0.5 = 1.1544",
  { x: 0.6, y: 5.9, w: 6.3, h: 0.8, fontSize: 11, color: "000000", fontFace: FONT, margin: 0.1 }
);
s.addText("Net6", { x: 0.6, y: 5.9, w: 0.8, h: 0.3, fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("Net7", { x: 0.6, y: 6.25, w: 0.8, h: 0.3, fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// Green equation boxes (O calculations)
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.5, y: 4.6, w: 5.0, h: 1.2,
  fill: { color: "FFFFFF" }, line: { color: "00B050", width: 1.5 },
});
s.addText(
  "O3 = 1 / (1 + e^-2.3) = 0.909\nO4 = 1 / (1 + e^-3.4) = 0.968\nO5 = 1 / (1 + e^-4.5) = 0.989",
  { x: 7.6, y: 4.6, w: 4.8, h: 1.2, fontSize: 11, color: "000000", fontFace: FONT, margin: 0.1 }
);
s.addText("O3", { x: 7.6, y: 4.6, w: 0.8, h: 0.3, fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("O4", { x: 7.6, y: 4.9, w: 0.8, h: 0.3, fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("O5", { x: 7.6, y: 5.2, w: 0.8, h: 0.3, fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

s.addShape(pres.shapes.RECTANGLE, {
  x: 7.5, y: 5.9, w: 5.0, h: 0.8,
  fill: { color: "FFFFFF" }, line: { color: "00B050", width: 1.5 },
});
s.addText(
  "O6 = 1 / (1 + e^-1.1544) = 0.76\nO7 = 1 / (1 + e^-1.1544) = 0.76",
  { x: 7.6, y: 5.9, w: 4.8, h: 0.8, fontSize: 11, color: "000000", fontFace: FONT, margin: 0.1 }
);
s.addText("O6", { x: 7.6, y: 5.9, w: 0.8, h: 0.3, fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("O7", { x: 7.6, y: 6.25, w: 0.8, h: 0.3, fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

const outPath = "slide_030_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));