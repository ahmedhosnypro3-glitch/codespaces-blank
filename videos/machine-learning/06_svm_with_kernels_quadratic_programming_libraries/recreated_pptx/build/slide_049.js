// slide_049.js — Four point clusters with sparse red dots top-right
const { newPres, addHouseChrome, addPlotShell, addCluster, addRing, addLegend, W, H } = require("./shared.js");

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, 49, "SVM Kernel Visualization — Four-Cluster Structure");

const m = addPlotShell(pres, s, 1.5, 1.0, 11.0, 6.0, 0, 40, 0, 35, "Feature 1", "Feature 2");

// Red outer ring
addRing(pres, s, m, 20, 17.5, 14, 14, "FF0000", 0.04);

// Blue left-center blob
addCluster(pres, s, m, 12, 17.5, 8, 50, "0000FF", 0.04);

// Black right-center blob
addCluster(pres, s, m, 28, 17.5, 8, 50, "000000", 0.04);

// Sparse red dots top-right
for (let i = 0; i < 15; i++) {
  const x = 30 + Math.random() * 8;
  const y = 25 + Math.random() * 8;
  const px = m.toX(x);
  const py = m.toY(y);
  s.addShape(pres.shapes.OVAL, { x: px - 0.04, y: py - 0.04, w: 0.08, h: 0.08, fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 } });
}

addLegend(pres, s, 1.7, 1.2, [
  { text: "● Red outer ring", color: "FF0000" },
  { text: "● Blue cluster (class 1)", color: "0000FF" },
  { text: "● Black cluster (class 2)", color: "000000" },
  { text: "● Sparse red (outliers)", color: "FF0000" },
]);

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_049_recreated.pptx" })
  .then(() => console.log("wrote slide_049_recreated.pptx"))
  .catch(err => console.error(err));