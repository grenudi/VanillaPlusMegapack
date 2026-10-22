#!/usr/bin/env python3
"""Draws the MHGA (Make Helldivers Great Again) README banner, 2172x724, in code.

Same visual direction as the upstream Vanilla Plus Megapack banner (see
assets/ARTWORK.md "Banner"): pure typography on a distressed charcoal ground,
wide heavy cream + yellow block type in two stacked lines, clipped yellow border
rules that step at the right (top) and left (bottom), three yellow hazard slashes
bottom left, yellow wear in the corners, small letter-spaced cream footer.

Deterministic: the same inputs give the same pixels. Needs Pillow, NumPy, SciPy and
the two OFL fonts in ./fonts (Archivo Black for the title, Barlow Condensed
SemiBold for the footer; licenses alongside).

    python banner.py                 # writes banner.png next to this file
    python banner.py --out x.png --footer "your footer text"
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy.ndimage import gaussian_filter

W, H = 2172, 724
GROUND = np.array([18, 17, 16], float)        # #121110
CREAM = np.array([240, 232, 214], float)      # #f0e8d6
YELLOW = np.array([253, 208, 12], float)      # #fdd00c
HERE = Path(__file__).resolve().parent
LINE_1, LINE_2 = "Make Helldivers", "Great Again"
FOOTER = "Fork of Vanilla Plus Megapack by CowboyBingus"
SEED = 1984
SQUEEZE = 0.80   # horizontal squeeze of the wide title face


def field(rng, sigma):
    """Unit-variance smooth noise."""
    n = gaussian_filter(rng.standard_normal((H, W)), sigma)
    return n / n.std()


def corner_weight(power=2.2):
    """0..1, strongest in the four corners (where the wear is)."""
    y, x = np.mgrid[0:H, 0:W]
    dx = np.minimum(x, W - 1 - x) / (W * 0.13)
    dy = np.minimum(y, H - 1 - y) / (H * 0.40)
    return np.exp(-(dx ** power + dy ** power) ** 0.5 * 2.3)


def texture(rng):
    lum = 0.4 * field(rng, 1.1) + 0.45 * field(rng, 3.5) + 1.0 * field(rng, 14) + 0.9 * field(rng, 55) + 0.6 * field(rng, 160)
    img = GROUND[None, None, :] + lum[..., None] * 6.5
    speck = rng.random((H, W))
    img += ((speck > 0.9795) * rng.uniform(25, 85, (H, W)))[..., None]       # bright grit
    img -= ((speck < 0.012) * rng.uniform(6, 14, (H, W)))[..., None]         # dark pits
    # fine diagonal scratches, lower-left to upper-right like the original
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    for _ in range(380):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        a = np.deg2rad(rng.uniform(36, 56))
        ln = rng.uniform(30, 280)
        d.line([(x, y), (x + ln * np.cos(a), y - ln * np.sin(a))], fill=int(rng.uniform(25, 85)), width=1)
    img += gaussian_filter(np.asarray(layer, float), 0.55)[..., None] * 0.55
    # yellow wear: dots and short scratches, thickest in the corners
    wear = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(wear)
    cw = corner_weight()
    for _ in range(16000):
        x, y = int(rng.uniform(0, W)), int(rng.uniform(0, H))
        if rng.random() < cw[y, x] * 0.95:
            if rng.random() < 0.35:
                a = np.deg2rad(rng.uniform(38, 58)); ln = rng.uniform(6, 70)
                d.line([(x, y), (x + ln * np.cos(a), y - ln * np.sin(a))], fill=int(rng.uniform(70, 210)), width=1)
            else:
                r = rng.uniform(0.4, 1.8)
                d.ellipse([x - r, y - r, x + r, y + r], fill=int(rng.uniform(80, 230)))
    wear = np.asarray(wear, float) / 255.0 * 0.85
    img = img * (1 - wear[..., None]) + YELLOW[None, None, :] * 0.9 * wear[..., None]
    # vignette
    y, x = np.mgrid[0:H, 0:W]
    vig = 1 - 0.30 * (((x - W / 2) / (W / 2)) ** 2 * 0.7 + ((y - H / 2) / (H / 2)) ** 2 * 0.5)
    return img * vig[..., None]


def worn(rng, alpha):
    """Knock small flecks out of a layer so rules and slashes look scuffed."""
    n = field(rng, 0.9) + 0.6 * field(rng, 3.0)
    return alpha * np.clip(1.25 - (n > 1.35) * 1.0 - (n > 1.9) * 1.0, 0.0, 1.0)


def rules_and_slashes(rng):
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    top = [(0, 76), (1925, 76), (2008, 155), (W, 155)]
    bottom = [(0, 568), (372, 568), (423, 626), (W, 626)]
    for pts in (top, bottom):
        d.line(pts, fill=255, width=5, joint="curve")
    for i in range(3):                                   # three hazard slashes
        x0, y0, y1, w, skew = 78 + i * 76, 600, 647, 46, 32
        d.polygon([(x0, y1), (x0 + w, y1), (x0 + w + skew, y0), (x0 + skew, y0)], fill=255)
    a = np.asarray(layer.filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0
    return worn(rng, a)


def fit_font(path, text, target_w):
    lo, hi = 20, 600
    while hi - lo > 1:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(str(path), mid)
        if f.getbbox(text)[2] - f.getbbox(text)[0] > target_w:
            hi = mid
        else:
            lo = mid
    return ImageFont.truetype(str(path), lo)


def title_layer(path, text, target_w, squeeze, cx, top):
    """Title line fitted to target_w after a horizontal squeeze (taller, heavier letters)."""
    font = fit_font(path, text, target_w / squeeze)
    bb = font.getbbox(text)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    tmp = Image.new("L", (w, h), 0)
    ImageDraw.Draw(tmp).text((-bb[0], -bb[1]), text, font=font, fill=255)
    tmp = tmp.resize((round(w * squeeze), h), Image.LANCZOS)
    layer = Image.new("L", (W, H), 0)
    layer.paste(tmp, (round(cx - tmp.width / 2), round(top)))
    return np.asarray(layer, float) / 255.0, h


def distress(rng, mask):
    """Cracks (thin zero-crossing lines of smooth noise), pits and grain inside the letters."""
    cracks = (np.abs(field(rng, 2.2)) < 0.07) * (field(rng, 9) > 0.1)
    pits = field(rng, 0.8) > 2.6
    cut = np.clip(cracks * 0.85 + pits * 0.9, 0, 1)
    return mask * (1 - cut), 0.93 + 0.05 * field(rng, 5) + 0.03 * field(rng, 1.0)


def footer_mask(font, text, cx, cy, tracking):
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, cy), ch, font=font, fill=255, anchor="lm")
        x += w + tracking
    return np.asarray(layer, float) / 255.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "banner.png"))
    ap.add_argument("--footer", default=FOOTER)
    args = ap.parse_args()
    rng = np.random.default_rng(SEED)
    img = texture(rng)

    title_font = HERE / "fonts" / "ArchivoBlack-Regular.ttf"
    foot_font = ImageFont.truetype(str(HERE / "fonts" / "BarlowCondensed-SemiBold.ttf"), 44)
    cx = W / 2
    m1, h1 = title_layer(title_font, LINE_1, 1660, SQUEEZE, cx, 104)
    m2, _ = title_layer(title_font, LINE_2, 1520, SQUEEZE, cx, 104 + h1 + 8)

    shadow = gaussian_filter(np.roll(np.roll(np.maximum(m1, m2), 9, axis=0), 6, axis=1), 11)
    img *= (1 - 0.7 * shadow)[..., None]
    for m, color in ((m1, CREAM), (m2, YELLOW)):
        m = gaussian_filter(m, 0.7)
        md, tone = distress(rng, m)
        col = color[None, None, :] * tone[..., None]
        img = img * (1 - md[..., None]) + col * md[..., None]

    fm = gaussian_filter(footer_mask(foot_font, args.footer, cx, 594, 6.0), 0.5)
    img = img * (1 - fm[..., None]) + CREAM[None, None, :] * 0.96 * fm[..., None]

    ru = rules_and_slashes(rng)
    img = img * (1 - ru[..., None]) + YELLOW[None, None, :] * ru[..., None]

    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").save(args.out, optimize=True)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
