// slide_054.js — 16 2x2 blue/red dot groupings on lattice
const { newPres, addHouseChrome, addPlotShell, addCluster, addDot, addLegend, W, H } = require("./shared.js");

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, 54, "SVM Kernel Visualization — Lattice of Decision Regions");

const m = addPlotShell(pres, s, 1.5, 1.0, 11.0, 6.0, 0, 25, 0, 25, "Feature 1", "Feature 2");

// 16 2x2 dot groupings on ~5-unit lattice
const latticeCenters = [
  [3, 20], [8, 20], [13, 20], [18, 20],
  [3, 15], [8, 15], [13, 15], [18, 15],
  [3, 10], [8, 10], [13, 10], [18, 10],
  [3, 5], [8, 5], [13, 5], [18, 5],
];

latticeCenters.forEach(([cx, cy], idx) => {
  const color = (idx % 2 === 0) ? "0000FF" : "FF0000";  // alternating blue/red
  // 2x2 grid
  for (let dx = -0.8; dx <= 0.8; dx += 1.6) {
    for (let dy = -0.8; dy <= 0.8; dy += 1.6) {
      addDot(pres, s, m, cx + dx, cy + dy, color, 0.04);
    }
  }
});

// Gray arrow cursor (from vision) - omit as it's an artifact
// s.addText("▶", { x: m.toX(18), y: m.toY(19), w: 0.3, h: 0.3, fontSize: 14, color: "888888", fontFace: "Arial", margin: 0 });

addLegend(pres, s, 1.7, 1.2, [
  { text: "● Blue dot clusters", color: "0000FF" },
  { text: "● Red dot clusters", color: "FF0000" },
]);

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_054_recreated.pptx" })
  .then(() => console.log("wrote slide_054_recreated.pptx"))
  .catch(err => console.error(err));