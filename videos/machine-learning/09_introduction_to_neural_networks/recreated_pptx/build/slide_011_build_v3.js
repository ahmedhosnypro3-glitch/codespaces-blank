// Slide 011: Classification of "AND" Truth Table — full-fidelity rebuild
// All geometry/colors measured from the original frame (see qa/slide011/ forensics).
const pptxgen = require("pptxgenjs");
const V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/";

const NUM = 11;
const BG = "E8E8E8";        // slide background (house rule + measured #E8E8E8 inside frame)
const RED = "C00000";       // table border, arrows, diamond, bias label
const TITLE_RED = "990000"; // measured title/axis red
const BLACK = "000000";
const GREY = "808080";
const TEXT_GREY = "333333";
const WEIGHT_BLUE = "1E00B8";
const CYAN_PILL = "B8FFFD";
const TEAL_TXT = "18685F";
const GREEN_PILL = "BAFFB4";
const GREEN_TXT = "044E00";
const MINT = "E4FFFA";
const MINT_LINE = "5FCFC0";
const PINK = "FFE2FE";
const PINK_LINE = "E08FD8";
const CREAM = "FCFFE2";
const CREAM_LINE = "E8E8B0";
const CARD_LINE = "C0A0A4";
const EQ_FILL = "F7E8D3";
const EQ_LINE = "B8948A";
const YELLOW = "FFF9C4";
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: BG };

// 1. house frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});

// 2. badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: TEXT_GREY, fontFace: FONT, margin: 0,
});

// 3. title (house chrome: x 0.6, y 0.28, w 12.13)
s.addText("Classification of \u201CAND\u201D Truth Table", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// 4. truth table — px (96..314) x (138..307)
const TX = 0.737, TY = 1.584, TW = 3.365, TH = 2.578;
const CX = [TX, 1.818, 2.929, TX + TW];
const RY = [TY, 2.164, 2.720, 3.193, 3.704, TY + TH];
s.addShape(pres.shapes.RECTANGLE, {
  x: TX, y: TY, w: TW, h: TH, fill: { type: "none" }, line: { color: RED, width: 2 },
});
for (let i = 1; i < 3; i++) {
  s.addShape(pres.shapes.LINE, {
    x: CX[i], y: TY, w: 0, h: TH, line: { color: GREY, width: 0.75 },
  });
}
for (let r = 1; r < 5; r++) {
  s.addShape(pres.shapes.LINE, {
    x: TX, y: RY[r], w: TW, h: 0, line: { color: GREY, width: 0.75 },
  });
}
const HDR = [[{ t: "X" }, { t: "1", options: { subscript: true } }],
             [{ t: "X" }, { t: "2", options: { subscript: true } }],
             [{ t: "O/P" }]];
for (let c = 0; c < 3; c++) {
  s.addText(HDR[c], {
    x: CX[c], y: RY[0], w: CX[c + 1] - CX[c], h: RY[1] - RY[0],
    align: "center", valign: "middle", fontSize: 24, bold: true,
    color: BLACK, fontFace: FONT, margin: 0,
  });
}
const ROWS = [["0", "0", "0"], ["0", "1", "0"], ["1", "0", "0"], ["1", "1", "1"]];
for (let r = 0; r < 4; r++) {
  for (let c = 0; c < 3; c++) {
    s.addText(ROWS[r][c], {
      x: CX[c], y: RY[r + 1], w: CX[c + 1] - CX[c], h: RY[r + 2] - RY[r + 1],
      align: "center", valign: "middle", fontSize: 18,
      color: BLACK, fontFace: FONT, margin: 0,
    });
  }
}
// O/P highlight pills (cyan x3, green x1) with matching dark digits
const PW = 0.370, PH = 0.42, PXC = 3.5155;
for (let r = 0; r < 4; r++) {
  const yc = (RY[r + 1] + RY[r + 2]) / 2;
  const green = (r === 3);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: PXC - PW / 2, y: yc - PH / 2, w: PW, h: PH,
    fill: { color: green ? GREEN_PILL : CYAN_PILL },
    line: { color: green ? GREEN_PILL : CYAN_PILL, width: 0.75 },
    rectRadius: 0.08,
  });
  s.addText(ROWS[r][2], {
    x: PXC - PW / 2, y: yc - PH / 2, w: PW, h: PH,
    align: "center", valign: "middle", fontSize: 18, bold: true,
    color: green ? GREEN_TXT : TEAL_TXT, fontFace: FONT, margin: 0,
  });
}

// 5. decision-boundary plot image (matplotlib, card px 539..839 x 111..367)
s.addImage({
  path: V + "plot_s011.png", x: 7.576, y: 1.172, w: 4.631, h: 3.904,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.576, y: 1.172, w: 4.631, h: 3.904,
  fill: { type: "none" }, line: { color: CARD_LINE, width: 0.75 },
});

// 6. perceptron diagram panel (px 144..511 x 355..489)
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.478, y: 4.894, w: 5.665, h: 2.044,
  fill: { color: "FFFFFF" }, line: { color: CARD_LINE, width: 0.75 },
});
const sub = (l) => [{ t: l }, { t: "1", options: { subscript: true } }];
const sub2 = (l) => [{ t: l }, { t: "2", options: { subscript: true } }];
const INP = [
  { runs: sub("x"), x: 1.833, y: 5.16 },
  { runs: sub2("x"), x: 1.833, y: 5.785 },
];
for (const it of INP) {
  s.addText(it.runs, { x: it.x, y: it.y, w: 0.6, h: 0.25, fontSize: 14, color: BLACK, fontFace: FONT, margin: 0 });
}
s.addText("-5", { x: 2.450, y: 5.05, w: 0.6, h: 0.25, fontSize: 14, color: WEIGHT_BLUE, fontFace: FONT, margin: 0 });
s.addText("-3", { x: 2.450, y: 5.94, w: 0.6, h: 0.25, fontSize: 14, color: WEIGHT_BLUE, fontFace: FONT, margin: 0 });
s.addText("1", { x: 1.848, y: 6.555, w: 0.35, h: 0.25, fontSize: 14, color: RED, fontFace: FONT, margin: 0 });
s.addText("6", { x: 2.558, y: 6.58, w: 0.35, h: 0.25, fontSize: 14, color: WEIGHT_BLUE, fontFace: FONT, margin: 0 });
// connectors
s.addShape(pres.shapes.LINE, { x: 2.033, y: 5.245, w: 1.768, h: 0.648, line: { color: "C9C4C4", width: 0.75 } });
s.addShape(pres.shapes.LINE, { x: 2.033, y: 5.893, w: 1.768, h: 0, line: { color: "C9C4C4", width: 0.75 } });
s.addShape(pres.shapes.LINE, { x: 2.033, y: 6.648, w: 1.768, h: -0.755, line: { color: "C9C4C4", width: 0.75 } });
// convergence diamond + Sigma circle
s.addShape(pres.shapes.DIAMOND, { x: 3.745, y: 5.818, w: 0.112, h: 0.150, fill: { color: RED }, line: { color: RED, width: 0.5 } });
s.addShape(pres.shapes.OVAL, { x: 3.870, y: 5.626, w: 0.602, h: 0.549, fill: { color: MINT }, line: { color: MINT_LINE, width: 1 } });
s.addText("\u03A3", { x: 3.870, y: 5.626, w: 0.602, h: 0.549, align: "center", valign: "middle", fontSize: 26, bold: true, color: BLACK, fontFace: FONT, margin: 0 });
// arrow -> step box
s.addShape(pres.shapes.LINE, { x: 4.472, y: 5.893, w: 0.294, h: 0, line: { color: RED, width: 2.25, endArrowType: "triangle" } });
// step-function box with blue step glyph
s.addShape(pres.shapes.RECTANGLE, { x: 4.766, y: 5.657, w: 0.648, h: 0.488, fill: { color: PINK }, line: { color: PINK_LINE, width: 1 } });
s.addShape(pres.shapes.RECTANGLE, { x: 4.982, y: 5.793, w: 0.016, h: 0.255, fill: { color: WEIGHT_BLUE }, line: { color: WEIGHT_BLUE, width: 0.5 } });
s.addShape(pres.shapes.RECTANGLE, { x: 4.982, y: 5.793, w: 0.150, h: 0.032, fill: { color: WEIGHT_BLUE }, line: { color: WEIGHT_BLUE, width: 0.5 } });
s.addShape(pres.shapes.RECTANGLE, { x: 4.948, y: 6.021, w: 0.184, h: 0.032, fill: { color: WEIGHT_BLUE }, line: { color: WEIGHT_BLUE, width: 0.5 } });
// activation rule label above the box — original glyphs measured at
// x361..402 / y372..396 (960-space): line 1 ">0 ⇒ 1", line 2 "≤0 ⇒ 0".
// NOTE: never pass this as a run array with an embedded \n — it silently
// produces no <a:t> in the slide XML and renders empty.
s.addShape(pres.shapes.RECTANGLE, { x: 4.781, y: 5.104, w: 0.741, h: 0.461, fill: { color: CREAM }, line: { color: CREAM_LINE, width: 0.5 } });
s.addText(">0 \u21D2 1", {
  x: 4.781, y: 5.104, w: 0.741, h: 0.2305,
  align: "center", valign: "middle", fontSize: 10, color: TEXT_GREY, fontFace: FONT, margin: 0,
});
s.addText("\u22640 \u21D2 0", {
  x: 4.781, y: 5.3345, w: 0.741, h: 0.2305,
  align: "center", valign: "middle", fontSize: 10, color: TEXT_GREY, fontFace: FONT, margin: 0,
});
// arrow -> O/P
s.addShape(pres.shapes.LINE, { x: 5.414, y: 5.893, w: 1.004, h: 0, line: { color: RED, width: 2.25, endArrowType: "triangle" } });
s.addText("O/P", { x: 6.557, y: 5.79, w: 0.6, h: 0.25, fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0 });

// 7. equation card + box — measured peach fill px 583..822 x 409..472,
// equation ink px 596..810 x 428..452 (960-space)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 8.097, y: 5.682, w: 3.320, h: 0.874,
  fill: { color: EQ_FILL }, line: { color: EQ_LINE, width: 1 }, rectRadius: 0.08,
});
s.addImage({
  path: V + "eq_s011_dX.png", x: 8.425, y: 5.992, w: 2.66333, h: 0.25333,
});

pres.writeFile({ fileName: V + "slide_011_recreated.pptx" }).then(() => console.log("wrote slide_011_recreated.pptx"));
