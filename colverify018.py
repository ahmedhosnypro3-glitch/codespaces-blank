from PIL import Image
V="/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
B=f"{V}/recreated_pptx/build"
S=300/72.0
im=Image.open(f"{B}/slide_018_unipolar_step.png").convert("RGB")
x0,y0=70,168
for fx in (110,150,250):
    print(f"--- uni column frame x={fx}")
    for fy in range(219,232):
        q,p=int(round((fx-x0)*S)),int(round((fy-y0)*S))
        print(f"   y{fy} png{p} {im.getpixel((q,p))}")
print("--- uni high plateau column frame x=250")
for fy in range(191,199):
    q,p=int(round((250-x0)*S)),int(round((fy-y0)*S))
    print(f"   y{fy} png{p} {im.getpixel((q,p))}")
im2=Image.open(f"{B}/slide_018_bipolar_step.png").convert("RGB")
bx0,by0=509,168
for fx in (580,650):
    print(f"--- bip column frame x={fx}")
    for fy in range(246,256):
        q,p=int(round((fx-bx0)*S)),int(round((fy-by0)*S))
        print(f"   y{fy} png{p} {im2.getpixel((q,p))}")
