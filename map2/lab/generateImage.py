import json

from PIL import Image

src = '../assets/202.jpg'

mw = 32 * 60
mh = 32 * 50

out = Image.new('RGBA', (mw, mh))
im = Image.open(src)

for i in range(60):
    for j in range(50):
        x = i * 32
        y = j * 32
        out.paste(im, (x, y))

out.save("image.png")
out.show()