// slide_048.js — Three scatter clusters with red C-shape
const { newPres, addHouseChrome, addPlotShell, addCluster, addRing, addLegend, W, H } = require("./shared.js");

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, 48, "SVM Kernel Classes — Three-Cluster Visualization");

const m = addPlotShell(pres, s, 1.5, 1.0, 11.0, 6.0, 0, 40, 0, 35, "Feature 1", "Feature 2");

// Red C-shape (large C enclosing others)
addRing(pres, s, m, 20, 17.5, 14, 14, "FF0000", 0.04);

// Blue dense blob left-center
addCluster(pres, s, m, 12, 17.5, 8, 60, "0000FF", 0.04);

// Black dense blob right-center
addCluster(pres, s, m, 28, 17.5, 8, 60, "000000", 0.04);

addLegend(pres, s, 1.7, 1.2, [
  { text: "● Red C-shape (outer boundary)", color: "FF0000" },
  { text: "● Blue cluster (class 1)", color: "0000FF" },
  { text: "● Black cluster (class 2)", color: "000000" },
]);

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_048_recreated.pptx" })
  .then(() => console.log("wrote slide_048_recreated.pptx"))
  .catch(err => console.error(err));