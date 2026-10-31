#!/usr/bin/env python3
import sys
import numpy as np
from PIL import Image

def content_box(path, label):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    h, w = a.shape[:2]
    r, g, b = a[...,0], a[...,1], a[...,2]
    lum = a.mean(axis=2)
    # The slide page area is a mid-light gray (~231-233), clearly darker than
    # the near-white video margin (>=250) and lighter than the black bar (<40).
    page = (lum > 150) & (lum < 248)
    # near-white margin
    white = lum >= 248
    black = lum < 60
    print("%s %dx%d  white=%.1f%% black=%.1f%%" % (label, w, h, 100*white.mean(), 100*black.mean()))
    rows_page = page.sum(axis=1); cols_page = page.sum(axis=0)
    rows = np.nonzero(rows_page > 0.5*w)[0]
    cols = np.nonzero(cols_page > 0.3*h)[0]
    print("  page rows>50%%: %s..%s" % (rows.min() if rows.size else -1, rows.max() if rows.size else -1))
    print("  page cols>30%%: %s..%s" % (cols.min() if cols.size else -1, cols.max() if cols.size else -1))
    # white margin extents per row of content
    wrows = np.nonzero(white.sum(axis=1) > 0.5*w)[0]
    print("  white rows>50%%: %s" % wrows.tolist()[:10])
    wcols = np.nonzero(white.sum(axis=0) > 0.3*h)[0]
    print("  white cols>30%%: %s" % wcols.tolist()[:20])
    brows = np.nonzero(black.sum(axis=1) > 0.5*w)[0]
    print("  black rows>50%%: %s" % brows.tolist()[:5], "..", brows.tolist()[-5:] if brows.size else [])

for s in ["001","004","005","006","007"]:
    content_box("unique_slides/slide_%s.jpg" % s, "ORIG%s" % s)
