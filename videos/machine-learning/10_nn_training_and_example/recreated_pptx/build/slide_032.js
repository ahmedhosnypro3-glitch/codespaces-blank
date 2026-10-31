// slide_032.js — "Initialized weights" / "Updated weights (after iteration #1)"
// Build: NODE_PATH=$(npm root -g) node slide_032.js
// Patterns: house-chrome, explicit-line-spacing
// Two stacked NN panels, measured: x101..824px, y89..285 (top), y330..525 (bottom)
const pptxgen = require("pptxgenjs");

const VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example";
const PX = 13.33 / 960;
const px = v => +(v * PX).toFixed(4);
const FONT = "Arial";
const BLACK = "000000", BLUE = "0000FF", RED = "C00000";
const GREEN = "00A651", MAGENTA = "A000A0", YELLOW = "FFFF99";
const PEACH = "F8CBAD", LIGHTBLUE = "9DC3E6";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ========== HOUSE CHROME ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("32", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// ========== HELPERS ==========
function txt(str, x, y, w, h, size, color, bold, align, italic, underline) {
  s.addText(str, {
    x, y, w, h, align: align || "left", valign: "middle",
    fontSize: size, bold: !!bold, italic: !!italic, underline: underline ? true : false,
    color, fontFace: FONT, margin: 0,
  });
}
function node(cx, cy, r, fill, stroke) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    fill: { color: fill }, line: { color: stroke, width: 1 },
  });
}
function dot(cx, cy, fill) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cx - 2), y: px(cy - 2), w: px(4), h: px(4),
    fill: { color: fill }, line: { color: fill, width: 0.5 },
  });
}
function conn(x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, {
    x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
    line: { color, width: 0.75 },
  });
}
// weight label placed at the midpoint of an edge, offset by (ox,oy) source px
function wlab(x1, y1, x2, y2, t, color, ox, oy) {
  const cx = (x1 + x2) / 2 + (ox || 0), cy = (y1 + y2) / 2 + (oy || 0);
  txt(t, px(cx - 22), px(cy - 7), px(44), px(14), 7, color, true, "center");
}

// panel in source-px coords: x0..x1, yTop of the panel border
function drawPanel(yTop, title, g, m, outVec, outDotX) {
  // red-bordered panel box
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(101), y: px(yTop), w: px(824 - 101), h: px(196),
    fill: { type: "none" }, line: { color: RED, width: 1.25 },
  });
  txt(title, px(110), px(yTop + 4), px(320), px(15), 12, RED, true, "left", true);

  // ---- input side ----
  txt("Input", px(115), px(yTop + 16), px(80), px(14), 10, BLUE, true, "left", true, true);
  txt("[", px(120), px(yTop + 32), px(10), px(56), 16, BLACK, true, "center");
  txt("1", px(132), px(yTop + 38), px(13), px(16), 10, BLACK, true, "center");
  txt("5", px(132), px(yTop + 76), px(13), px(16), 10, BLACK, true, "center");
  txt("]", px(146), px(yTop + 32), px(10), px(56), 16, BLACK, true, "center");
  txt("x1", px(120), px(yTop + 30), px(14), px(12), 8, BLUE, true, "center", true);
  txt("x2", px(120), px(yTop + 68), px(14), px(12), 8, BLUE, true, "center", true);

  node(190, yTop + 55, 6, BLACK, BLACK);
  node(190, yTop + 119, 6, BLACK, BLACK);
  dot(197, yTop + 55, RED); dot(197, yTop + 119, RED);
  node(185, yTop + 165, 7, LIGHTBLUE, BLUE);
  txt("1", px(178), px(yTop + 158), px(14), px(14), 8, BLACK, true, "center");
  txt("Bias", px(148), px(yTop + 160), px(32), px(12), 8, BLUE, true, "center", true);

  // ---- hidden layer ----
  const hy = [yTop + 35, yTop + 92, yTop + 148];
  const hidFills = [YELLOW, YELLOW, YELLOW];
  for (let i = 0; i < 3; i++) {
    node(344, hy[i], 11, hidFills[i], "7F7F7F");
    txt(String(3 + i), px(334), px(hy[i] - 7), px(20), px(14), 10, BLUE, true, "center");
    txt("O" + (3 + i), px(360), px(hy[i] - 22), px(24), px(12), 8, BLUE, true, "center");
    dot(333, hy[i], RED);
  }
  txt("Bias", px(300), px(yTop + 160), px(32), px(12), 8, BLUE, true, "center", true);
  node(344, yTop + 165, 7, LIGHTBLUE, BLUE);
  txt("1", px(337), px(yTop + 158), px(14), px(14), 8, BLACK, true, "center");
  dot(336, yTop + 165, RED);

  // ---- output layer ----
  const oy = [yTop + 67, yTop + 127];
  for (let i = 0; i < 2; i++) {
    node(551, oy[i], 10, PEACH, "7F7F7F");
    txt(String(6 + i), px(541), px(oy[i] - 7), px(20), px(14), 10, BLUE, true, "center");
  }
  txt("O6", px(567), px(oy[0] - 22), px(24), px(12), 8, BLUE, true, "center");
  txt("O7", px(567), px(oy[1] - 22), px(24), px(12), 8, BLUE, true, "center");
  txt("Output", px(560), px(yTop + 5), px(60), px(14), 10, BLUE, true, "center", true, true);

  // ---- output vector + double arrow + target ----
  txt(String(outVec[0]), px(outDotX - 10), px(yTop + 55), px(34), px(16), 11, BLACK, true, "left");
  txt(String(outVec[1]), px(outDotX - 10), px(yTop + 110), px(34), px(16), 11, BLACK, true, "left");
  s.addShape(pres.shapes.LEFT_RIGHT_ARROW, {
    x: px(660), y: px(yTop + 86), w: px(34), h: px(14),
    fill: { color: RED }, line: { color: RED, width: 0.5 },
  });
  txt("Target", px(700), px(yTop + 5), px(60), px(14), 10, BLACK, true, "center", true, true);
  txt("0", px(716), px(yTop + 58), px(16), px(16), 11, BLACK, true, "center");
  txt("1", px(716), px(yTop + 112), px(16), px(16), 11, BLACK, true, "center");
  txt("t6", px(700), px(yTop + 62), px(20), px(12), 8, BLACK, true, "center");
  txt("t7", px(700), px(yTop + 116), px(20), px(12), 8, BLACK, true, "center");
  txt("η = 5", px(755), px(yTop + 165), px(60), px(16), 11, RED, true, "center");

  // ---- input -> hidden edges (green labels) ----
  const ix = [190, 190, 185], iy = [yTop + 55, yTop + 119, yTop + 165];
  const gsrc = ["x1", "x2", "b"];
  for (let a = 0; a < 3; a++) {
    for (let i = 0; i < 3; i++) {
      conn(ix[a] + 7, iy[a], 344 - 11, hy[i], "A6A6A6");
      wlab(ix[a] + 7, iy[a], 344 - 11, hy[i], g[a][i], GREEN, gsrc[a] === "b" ? -22 : 0,
           gsrc[a] === "b" ? -6 : 0);
    }
  }
  // ---- hidden -> output edges (magenta labels) ----
  for (let a = 0; a < 4; a++) {
    const sx = a < 3 ? 344 : 344, sy = a < 3 ? hy[a] : yTop + 165;
    for (let i = 0; i < 2; i++) {
      conn(sx + 11, sy, 551 - 10, oy[i], "A6A6A6");
      wlab(sx + 11, sy, 551 - 10, oy[i], m[a][i], MAGENTA, 0, 0);
    }
  }
}

// ========== TOP PANEL: Initialized weights ==========
// Edge values cross-checked against slide 31's arithmetic (initial + ΔW = updated):
// x1 -> 3/4/5 = 0.1/0.2/0.3, x2 -> 3/4/5 = 0.4/0.5/0.6, bias -> 0.1/0.1/0.1
const gTop = [["0.1", "0.2", "0.3"], ["0.4", "0.5", "0.6"], ["0.1", "0.1", "0.1"]];
const mTop = [["0.3", "0.3"], ["0.4", "0.4"], ["0.5", "0.5"], ["0.2", "0.2"]];
drawPanel(89, "Initialized weights", gTop, mTop, ["0.791", "0.791"], 600);

// ========== BOTTOM PANEL: Updated weights (after iteration # 1) ==========
const gBot = [["0.125", "0.215", "0.305"], ["0.525", "0.575", "0.625"], ["0.125", "0.115", "0.105"]];
const mBot = [["-0.29", "-0.458"], ["-0.218", "-0.565"], ["-0.134", "-0.669"], ["-0.445", "-0.375"]];
drawPanel(330, "Updated weights (after iteration # 1)", gBot, mBot, ["0.352", "0.835"], 600);

pres.writeFile({ fileName: VID + "/recreated_pptx/slide_032_recreated.pptx" })
  .then(() => console.log("wrote slide_032_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
