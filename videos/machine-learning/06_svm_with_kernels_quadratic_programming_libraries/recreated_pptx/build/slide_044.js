const pptxgen = require("pptxgenjs");
const { newPres, addHouseChrome, addPlotShell, addDot, addCluster, addRing, W, H, FONT } = require("./shared.js");

const NUM = 44;
const TITLE = null;

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, NUM, TITLE);

// Main plot area with red border
// From analysis: x 0-50, y 0-30
const PX = 1.8, PY = 0.8, PW = 4.5, PH = 3.6;
const X_MIN = 0, X_MAX = 50;
const Y_MIN = 0, Y_MAX = 30;

const mapper = addPlotShell(pres, s, PX, PY, PW, PH, X_MIN, X_MAX, Y_MIN, Y_MAX, "", "");

// Four main clusters + red scatter
// Black cluster near (12, 20)
addCluster(pres, s, mapper, 12, 20, 4, 30, "000000", 0.045);

// Magenta cluster near (18, 20)
addCluster(pres, s, mapper, 18, 20, 4, 30, "FF00FF", 0.045);

// Green ring/blob near (15, 10) with solid cyan center
addRing(pres, s, mapper, 15, 10, 4, 4, "00FF00", 0.04);
addDot(pres, s, mapper, 15, 10, "00FFFF", 0.08);

// Blue cluster near (35, 17)
addCluster(pres, s, mapper, 35, 17, 5, 30, "0000FF", 0.045);

// Red dots sparsely distributed in region x=25 to 45, y=8 to 23
for (let x = 25; x <= 45; x += 1.5) {
  for (let y = 8; y <= 23; y += 1.5) {
    // Add some randomness
    const dx = x + (Math.random() - 0.5) * 1.5;
    const dy = y + (Math.random() - 0.5) * 1.5;
    addDot(pres, s, mapper, dx, dy, "FF0000", 0.03);
  }
}

// Small black arrow pointing to a red dot near (28, 21)
const arrX = mapper.toX(28);
const arrY = mapper.toY(21);
s.addShape(pres.shapes.LINE, { x: arrX, y: arrY + 0.5, w: 0, h: -0.5, line: { color: "000000", width: 1.5 } });
s.addShape(pres.shapes.LINE, { x: arrX - 0.1, y: arrY, w: 0.1, h: 0, line: { color: "000000", width: 1.5 } });
s.addShape(pres.shapes.LINE, { x: arrX + 0.1, y: arrY, w: -0.1, h: 0, line: { color: "000000", width: 1.5 } });

// Bottom black strip
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.15, w: W, h: 0.15,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_044_recreated.pptx" })
  .then(() => console.log("wrote slide_044_recreated.pptx"))
  .catch(e => console.error(e));