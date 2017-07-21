import json

from PIL import Image

src = '../assets/177.jpg'

x_blockCount = 70
y_blockCount = 120

mw = 32 * x_blockCount
mh = 32 * y_blockCount

out = Image.new('RGBA', (mw, mh))
im = Image.open(src)

for i in range(x_blockCount):
    for j in range(y_blockCount):
        x = i * 32
        y = j * 32
        out.paste(im, (x, y))

out.save("image.png")
out.show()