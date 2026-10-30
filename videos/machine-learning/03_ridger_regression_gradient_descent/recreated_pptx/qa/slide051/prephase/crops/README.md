# Prephase crop map — slide space (960x540, 1px = 1pt), 2x LANCZOS upscaled PNGs

| crop | slide-space box (x0,y0,x1,y1) | content |
|---|---|---|
| 048 topband   | 60,48,740,135  | top band box: input table, Initial W + REPEAT, check-classes Z table, legend |
| 048 aug_iter  | 58,135,265,315 | gray-framed Ugmented Vectors matrix + Iteration 1 red box |
| 048 calc_r12  | 268,135,860,275| calc rows 1-2 (d(x1) update row, d(x2)) |
| 048 calc_r56  | 268,400,860,532| calc rows 5-6 |
| 049 topband   | 60,48,740,135  | top band box: data table + Initial column + REPEAT + check grid + legend |
| 049 aug_stop  | 58,140,265,400 | Ugmented Vectors table + class labels + red Iteration 2 box + stop lines |
| 049 calc_r12  | 268,135,860,275| calc rows 1-2 (d(x1), d(x2) matrices) |
| 049 calc_r56  | 268,398,860,532| calc rows 5-6 |
| 050 topbox    | 60,48,740,135  | navy box: data table + math zone + colour legend |
| 050 pinkbox   | 735,50,845,180 | pink final-weight box (underlined W) |
| 050 aug_caption | 55,130,255,255 | caption box + augmented matrix + class row |
| 050 chart     | 300,165,835,495| scatter/line chart |
| 050 redstop   | 70,270,260,405 | red Iteration 2 box + stop text |
| 051 topcard   | 60,48,740,135  | pale card: sample matrix + Initial W + Step + legend + Z columns |
| 051 aug_redbox| 55,140,255,312 | Augmented Vectors matrix + red Check Classes box |
| 051 dec_r1    | 268,133,860,200| decision row 1 (d(Z1)) |
| 051 dec_r23   | 268,200,860,335| decision rows 2-3 |

To map a crop pixel back to slide space: slide_x = x0 + crop_x/2, slide_y = y0 + crop_y/2.
