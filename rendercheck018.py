from PIL import Image
V="/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
B=f"{V}/recreated_pptx/build"
orig=Image.open(f"{V}/unique_slides/slide_018.jpg").convert("RGB")
rend=Image.open(f"{B}/slide_018_rejudge_rendered-1.png").convert("RGB")
def rx(o): return int(round((0.15+(o-57)/846*13.03)*150.13))
def ry(o): return int(round((0.15+(o-43)/474*7.2)*150))
print("IMAGE SIZES: orig",orig.size,"rend",rend.size)
print("render mapping: orig(645,225)->render",(rx(645),ry(225)))
print("=== UNI low plateau: orig vs render column x=150")
for oy in range(222,228):
    print(f"  y{oy}: orig {orig.getpixel((150,oy))}  rend {rend.getpixel((rx(150),ry(oy)))}")
print("=== UNI high plateau: orig vs render column x=250")
for oy in range(192,198):
    print(f"  y{oy}: orig {orig.getpixel((250,oy))}  rend {rend.getpixel((rx(250),ry(oy)))}")
print("=== BIP high plateau: orig vs render column x=680")
for oy in range(192,198):
    print(f"  y{oy}: orig {orig.getpixel((680,oy))}  rend {rend.getpixel((rx(680),ry(oy)))}")
print("=== BIP low plateau: orig vs render column x=600")
for oy in range(249,256):
    print(f"  y{oy}: orig {orig.getpixel((600,oy))}  rend {rend.getpixel((rx(600),ry(oy)))}")
print("=== UNI jump column x=194..196 (orig) vs rx(194)/rx(195)")
for oy in range(206,222,3):
    print(f"  y{oy}: orig194 {orig.getpixel((194,oy))} orig195 {orig.getpixel((195,oy))}  rend{rx(194)} {rend.getpixel((rx(194),ry(oy)))} rend{rx(195)} {rend.getpixel((rx(195),ry(oy)))}")
print("=== shaft below low plateau (bip) x=644..645")
for oy in range(256,268,2):
    print(f"  y{oy}: orig644 {orig.getpixel((644,oy))} rend{rx(644)} {rend.getpixel((rx(644),ry(oy)))}")
