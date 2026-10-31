

def S(name, latex, color):
    return Shard(name, latex, color)


R, B, G, K = RED, BLUE, GREEN, BLACK
EQ = {}
EQ["r1L"] = piecewise("eq_r1L.png",
    [S("r1L_1", r"f(x)=", K), S("r1L_2", r"Rectified Linear U", R), S("r1L_3", r"nit=", K)],
    [([S("r1L_v0", r"0", R)], [S("r1L_c0", r"for\ x<0", K)]),
     ([S("r1L_v1", r"x", R)], [S("r1L_c1", r"for\ x\geq 0", G)])])
EQ["r1R"] = piecewise("eq_r1R.png",
    [S("r1R_0", r"f^{\prime}(x)=", K)],
    [([S("r1R_v0", r"0", R)], [S("r1R_c0", r"for\ x<0", K)]),
     ([S("r1R_v1", r"1", R)], [S("r1R_c1", r"for\ x\geq 0", G)])])
EQ["r2L"] = piecewise("eq_r2L.png",
    [S("r2L_1", r"f(x)=", K), S("r2L_2", r"P", B), S("r2L_3", r"arametric ReLU=", R)],
    [([S("r2L_v0", r"\alpha x", B)], [S("r2L_c0", r"for\ x<0", K)]),
     ([S("r2L_v1", r"x", R)], [S("r2L_c1", r"for\ x\geq 0", G)])])
EQ["r2R"] = piecewise("eq_r2R.png",
    [S("r2R_0", r"f^{\prime}(x)=", K)],
    [([S("r2R_v0", r"\alpha", B)], [S("r2R_c0", r"for\ x<0", K)]),
     ([S("r2R_v1", r"1", R)], [S("r2R_c1", r"for\ x\geq 0", G)])])
EQ["r3L"] = piecewise("eq_r3L.png",
    [S("r3L_1", r"f(x)=", K), S("r3L_2", r"E", B), S("r3L_3", r"xponential LU=", R)],
    [([S("r3L_v0a", r"\alpha(", B), S("r3L_v0b", r"e^{x}", R), S("r3L_v0c", r"-1)", K)],
      [S("r3L_c0", r"for\ x<0", K)]),
     ([S("r3L_v1", r"x", R)], [S("r3L_c1", r"for\ x\geq 0", G)])])
EQ["r3R"] = piecewise("eq_r3R.png",
    [S("r3R_0", r"f^{\prime}(x)=", K)],
    [([S("r3R_v0a", r"f(x)+", R), S("r3R_v0b", r"\alpha", B)], [S("r3R_c0", r"for\ x<0", K)]),
     ([S("r3R_v1", r"1", R)], [S("r3R_v1c", r"for\ x\geq 0", G)])])
EQ["r4L"] = simple("eq_r4L.png",
    [S("r4L_1", r"f(x)=", K), S("r4L_2", r"SoftPlus", R), S("r4L_3", r"=", K),
     S("r4L_4", r"\log_{e}(1+", K), S("r4L_5", r"e^{x}", R)])
EQ["r4R"] = fraction("eq_r4R.png",
    [S("r4R_0", r"f^{\prime}(x)=", K)], [S("r4R_n", r"1", K)],
    [S("r4R_d1", r"1+", K), S("r4R_d2", r"e^{-x}", R)], (0, 0, 0))
print("PITCH", PITCH)
for k, v in sorted(EQ.items()):
    print(k, v)
