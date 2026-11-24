"""Draw the app icons as PNG (phones need PNG to install the app).   Usage: python tools/make_icons.py"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
S = 2048  # draw big, shrink for smooth edges
K = S / 512


def draw(rounded):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    blue = (31, 111, 235, 255)
    if rounded:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(112 * K), fill=blue)
    else:
        d.rectangle([0, 0, S, S], fill=blue)
    pts = [(150 * K, 190 * K), (240 * K, 256 * K), (150 * K, 322 * K)]
    d.line(pts, fill="white", width=int(40 * K), joint="curve")
    r = 20 * K
    for x, y in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill="white")
    d.rounded_rectangle([270 * K, 302 * K, 380 * K, 342 * K], radius=int(20 * K), fill=(255, 212, 59, 255))
    return img


for name, size, rounded in [("icon-192.png", 192, True), ("icon-512.png", 512, True),
                            ("icon-maskable-512.png", 512, False), ("apple-touch-icon.png", 180, False)]:
    draw(rounded).resize((size, size), Image.LANCZOS).save(ROOT / name)
    print("wrote", name)
