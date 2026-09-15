"""Draws the Nexus images: a 1300x372 page header and a 1920x1080 gallery shot.

Nexus wants a wide header and a 16:9 gallery image, not the square Thunderstore icon,
so the paw trail from make_icon.py is re-laid out along the left with the title beside
it. Both sizes come out of one renderer with everything measured as a fraction of the
height, so the two stay the same picture at different shapes.

    python tools/make_banner.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_icon import BACKGROUND, FAINT, LEAD, TRAIL, paw  # noqa: E402

MEDIA = os.path.join(os.path.dirname(HERE), "media")
SCALE = 2


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def render(w, h, out):
    image = Image.new("RGBA", (w * SCALE, h * SCALE), BACKGROUND)

    # Same trail as the icon, walking up the left of the frame.
    for colour, scale, cx, cy, angle in [
        (FAINT, 0.13, 0.07, 0.86, -26),
        (TRAIL, 0.17, 0.16, 0.58, -17),
        (LEAD, 0.22, 0.27, 0.26, -8),
    ]:
        size = int(h * SCALE * scale * 1.7)
        layer = paw(size, colour).rotate(angle, resample=Image.BICUBIC, expand=True)
        image.alpha_composite(layer, (int(w * SCALE * cx - layer.width / 2),
                                      int(h * SCALE * cy - layer.height / 2)))

    draw = ImageDraw.Draw(image)
    title = font("C:/Windows/Fonts/segoeuib.ttf", int(h * SCALE * 0.103))
    sub = font("C:/Windows/Fonts/segoeui.ttf", int(h * SCALE * 0.047))

    x = int(w * SCALE * 0.34)
    draw.text((x, int(h * SCALE * 0.36)), "Cartur's", font=title, fill=(238, 232, 220, 255))
    draw.text((x, int(h * SCALE * 0.47)), "Follow Command", font=title, fill=LEAD)
    draw.text((x, int(h * SCALE * 0.61)), "Every tamed animal follows, not just wolves",
              font=sub, fill=(150, 140, 124, 255))

    image.resize((w, h), Image.LANCZOS).convert("RGB").save(out)
    print("wrote", out, (w, h))


render(1300, 372, os.path.join(MEDIA, "nexus-header.png"))
render(1920, 1080, os.path.join(MEDIA, "nexus-gallery.png"))
