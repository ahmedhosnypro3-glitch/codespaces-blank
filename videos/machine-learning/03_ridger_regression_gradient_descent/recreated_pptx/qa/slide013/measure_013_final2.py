#!/usr/bin/env python3
"""w013 truth-table measurement v2 — original slide_013.jpg only."""
from PIL import Image
import numpy as np
o = np.asarray(Image.open('unique_slides/slide_013.jpg').convert('RGB')).astype(int)

def med_region(x0, y0, x1, y1, label, exclude_dark=True):
    sub = o[y0:y1, x0:x1].reshape(-1, 3)
    if exclude_dark:
        keep = sub.max(axis=1) > 170
        sub = sub[keep]
    m = np.median(sub, axis=0).astype(int)
    print(f'{label}: median {tuple(m)} #{m[0]:02X}{m[1]:02X}{m[2]:02X} n={len(sub)}')

def scan_rows(x0, x1, y0, y1, label, thresh=0.85):
    print(f'{label} rows:')
    for y in range(y0, y1):
        row = o[y, x0:x1]
        nw = ((row[:,0]<235)|(row[:,1]<235)|(row[:,2]<235)).sum()
        if nw > (x1-x0)*thresh: print(f'  y={y} nw={nw}/{x1-x0}')

def scan_cols(y0, y1, x0, x1, label, thresh=0.6):
    print(f'{label} cols:')
    for x in range(x0, x1):
        col = o[y0:y1, x]
        nw = ((col[:,0]<235)|(col[:,1]<235)|(col[:,2]<235)).sum()
        if nw > (y1-y0)*thresh: print(f'  x={x} nw={nw}/{y1-y0}')

print('== TEST TABLE grid (x725..790 to avoid label box) ==')
scan_rows(725, 790, 120, 260, 'test band1')
scan_rows(725, 790, 260, 395, 'test band2')
scan_rows(725, 790, 395, 530, 'test band3')
scan_cols(135, 245, 714, 880, 'test band1')
print('\n== TEST y-row fill ==')
for bi,(y0,y1) in enumerate([(222,248),(355,385),(492,522)], start=1):
    med_region(725, y0, 868, y1, f'test band{bi} y-row fill')
print('\n== gridline core colours ==')
print('train v x133 rows160..186:', [tuple(o[y,133]) for y in (165,175,185)])
print('train h y157 cols 200..220:', [tuple(o[157,x]) for x in (200,210,220)])
print('test v x770 rows165..185:', [tuple(o[y,770]) for y in (170,180)])
print('test h y160 cols 730..760:', [tuple(o[160,x]) for x in (735,745,755)])
print('\n== LABEL BOX fill ==')
med_region(100, 100, 156, 121, 'Train fill', exclude_dark=False)
med_region(806, 100, 861, 121, 'Test fill', exclude_dark=False)
print('\n== ARROW core ==')
med_region(466, 193, 490, 204, 'left arrow shaft band1', exclude_dark=False)
med_region(630, 193, 655, 204, 'right arrow shaft band1', exclude_dark=False)
print('\n== ELLIPSE fill + text ==')
med_region(530, 218, 600, 244, 'ellipse band1 fill', exclude_dark=True)
med_region(530, 222, 600, 240, 'ellipse band1 text-dark', exclude_dark=False)
for bi,(x0,y0,x1,y1) in enumerate([(510,211,620,250),(515,350,620,388),(518,489,622,526)], start=1):
    sub = o[y0:y1, x0:x1]
    yel = (sub[:,:,0]>200)&(sub[:,:,1]>190)&(sub[:,:,2]<220)&(sub[:,:,0]-sub[:,:,2]>30)
    ys,xs = np.where(yel)
    print(f'ellipse band{bi} yellow bbox x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()}')
print('\n== TABLE TEXT ink heights (loose dark mask) ==')
def ink(x0,y0,x1,y1,label,pred=None):
    sub=o[y0:y1,x0:x1]
    if pred is None:
        m=sub.max(axis=2)<170
    else:
        m=pred(sub)
    ys,xs=np.where(m)
    if len(xs)==0: print(f'{label}: EMPTY'); return
    print(f'{label}: x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} w{xs.max()-xs.min()+1} h{ys.max()-ys.min()+1} n={len(xs)}')
def red(s): return (s[:,:,0]>110)&(s[:,:,1]<130)&(s[:,:,2]<130)&(s[:,:,0]-s[:,:,1]>40)
def blue(s): return (s[:,:,2]>100)&(s[:,:,2]-s[:,:,0]>40)
ink(134,127,173,157,'train hdr X1 (blue) X only', blue)
ink(134,127,173,157,'train hdr X1 all', None)
ink(174,127,214,157,'train hdr X2 all', red)
ink(134,158,174,188,'cell 1 (blue)')
ink(174,158,214,188,'cell 2 (red)')
ink(92,158,133,188,'rowlabel X1 (blue)', blue)
ink(719,158,770,189,'test 30')
ink(719,127,770,158,'test hdr Test1', red)
ink(719,188,770,220,'test 15')
print('\n== W box border thickness (band1) ==')
for x in range(500,515):
    col=o[130:245,x]
    n=(col.max(axis=1)<235).sum()
    if n: print(f'  x={x} nw={n}')
print('\n== TITLE font ink height by word ==')
ink(150,60,300,105,'title "Effect"', red)
ink(520,60,790,105,'title tail', red)
print('\n== BADGE ==')
ink(850,50,905,100,'badge numeral (dark)')
