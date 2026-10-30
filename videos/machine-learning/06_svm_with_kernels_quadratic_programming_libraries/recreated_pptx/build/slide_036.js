// slide_036.js — "How to Kernelize SVM" / Example: Quadratic Kernel
// Shared builder: build/kernel_example.js
// Run: node slide_036.js

const build = require("./kernel_example.js");

const EQ = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_036/";

build({
  num: 36,
  title: "How to Kernelize SVM",
  kicker: "Quadratic Kernel",
  eq: EQ,
  out: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_036_recreated.pptx",
  hlFill: "CCFFCC",
  clsFill: "FDEADA",
  clsBorder: "FF9900",
  connBorder: "E00000",
  bOrigW: 4.37333,
  bKW: 4.53,
  lagKW: 4.70667,
  kernelImg: { name: "eq_kernel_quad.png", w: 1.885, h: 0.35833 },
  classUpRuns: [
    { text: "W", options: { color: "000000" } },
    { text: "T", options: { color: "000000", superscript: true } },
    { text: " Z", options: { color: "000000" } },
  ],
  classLoRuns: [
    { text: "[W", options: { color: "000000" } },
    { text: "T", options: { color: "000000", superscript: true } },
    { text: " Z]", options: { color: "000000" } },
    { text: "2", options: { color: "000000", superscript: true } },
  ],
});
