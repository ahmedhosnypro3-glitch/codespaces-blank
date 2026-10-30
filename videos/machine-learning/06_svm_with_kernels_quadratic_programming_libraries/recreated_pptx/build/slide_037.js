// slide_037.js — "How to Kernelize SVM" / Example: Polynomial Kernel
// Shared builder: build/kernel_example.js
// Run: node slide_037.js

const build = require("./kernel_example.js");

const EQ = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_037/";

build({
  num: 37,
  title: "How to Kernelize SVM",
  kicker: "Polynomial Kernel",
  eq: EQ,
  out: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_037_recreated.pptx",
  hlFill: "99FF99",
  clsFill: "FFE0C0",
  clsBorder: null,
  connBorder: "808080",
  bOrigW: 4.22167,
  bKW: 5.32167,
  lagKW: 5.17833,
  kernelImg: null,
  kernelName: "eq_kernel_poly.png",
  kernelW: 2.53833,
  classUpRuns: [
    { text: "W", options: { color: "000000" } },
    { text: "T", options: { color: "000000", superscript: true } },
    { text: " Z", options: { color: "000000" } },
  ],
  classLoRuns: [
    { text: "[W", options: { color: "000000" } },
    { text: "T", options: { color: "000000", superscript: true } },
    { text: " Z + 1]", options: { color: "000000" } },
    { text: "d", options: { color: "000000", italic: true, superscript: true } },
  ],
});
