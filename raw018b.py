from PIL import Image
V="/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
o=Image.open(f"{V}/unique_slides/slide_018.jpg").convert("RGB")
print("=== BIPOLAR high plateau rows y 192..197, x 640..740")
for y in range(192,198):
    vals=[(x,o.getpixel((x,y))) for x in range(640,741,4)]
    print(f" y{y}: "+" ".join(f"{x}:{p[0]},{p[1]},{p[2]}" for x,p in vals))
print("=== BIPOLAR low plateau rows y 249..257, x 548..652")
for y in range(249,258):
    vals=[(x,o.getpixel((x,y))) for x in range(548,653,3)]
    print(f" y{y}: "+" ".join(f"{x}:{p[0]},{p[1]},{p[2]}" for x,p in vals))
print("=== UNIPOLAR jump column x 192..198, y 190..250")
for y in range(190,251,2):
    print(f" y{y}: "+" ".join(f"x{x}:{o.getpixel((x,y))}" for x in range(192,199)))
