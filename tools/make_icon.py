"""Draws the 256x256 Thunderstore icon.

Thunderstore rejects anything that is not exactly 256x256 PNG, and there is no art
asset to crop from, so the icon is drawn: a trail of paw prints walking off the
corner, brightest at the front. Two prints rather than one, because a single paw
says "animal" and a trail says "following".

    python tools/make_icon.py
"""
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "package", "icon.png")

SIZE = 256
SCALE = 4  # drawn large and downsampled, so the curves are not stair-stepped

BACKGROUND = (38, 34, 30, 255)
LEAD = (247, 205, 61, 255)     # the print nearest you
TRAIL = (138, 116, 52, 255)    # the one behind it, dimmer so the trail has a direction
FAINT = (78, 68, 44, 255)


def paw(size, colour):
    """One print on its own layer: a heel pad with four toes arced over it."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # Heel pad - wider than tall, sat low, with the top corners pulled in so it reads
    # as a pad rather than a circle.
    pad_w, pad_h = size * 0.62, size * 0.46
    cx = size / 2
    draw.ellipse([cx - pad_w / 2, size * 0.46, cx + pad_w / 2, size * 0.46 + pad_h], fill=colour)

    # Four toes on an arc above it. The outer two are smaller and set lower, which is
    # what stops the row looking like a line of identical dots.
    toes = [(-0.28, 0.28, 0.17), (-0.10, 0.15, 0.20), (0.10, 0.15, 0.20), (0.28, 0.28, 0.17)]
    for dx, dy, r in toes:
        w = size * r
        x, y = cx + size * dx, size * dy
        draw.ellipse([x - w / 2, y - w * 0.62, x + w / 2, y + w * 0.62], fill=colour)

    return layer


image = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), BACKGROUND)

# Back to front, so the lead print overlaps the one behind it rather than the reverse.
# Each is rotated slightly off vertical - a paw print squared to the frame looks stamped
# rather than walked - and each is placed by its centre, because rotate(expand=True)
# changes the layer size and a corner-based paste would then drift off the canvas.
prints = [
    (FAINT, 0.24, 0.22, 0.80, -26),
    (TRAIL, 0.31, 0.46, 0.54, -17),
    (LEAD,  0.40, 0.72, 0.26, -8),
]
for colour, scale, cx, cy, angle in prints:
    size = int(SIZE * SCALE * scale)
    layer = paw(size, colour).rotate(angle, resample=Image.BICUBIC, expand=True)
    image.alpha_composite(layer, (int(SIZE * SCALE * cx - layer.width / 2),
                                  int(SIZE * SCALE * cy - layer.height / 2)))

image = image.resize((SIZE, SIZE), Image.LANCZOS).convert("RGB")
image.save(OUT)
print("wrote", OUT, image.size)
