#!/usr/bin/env python3
"""Draws the MHGA box icon (1254x1254), the pack's own image in Arsenal and HD2MM.

Same layout as upstream's code-drawn icon (assets/source/pack_cover.py): big title on a dark ground, a yellow
bar with dark type, a hazard band, then a "packing slip" listing the bundled mods, each one ticked, running off
the edge so it stays true as the pack changes. Upstream renders it with Windows fonts; this draws it with the
OFL fonts in ./fonts so it can be regenerated anywhere. Deterministic.

    python thumbnail.py [--out thumbnail.png]
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter

N = 1254
HERE = Path(__file__).resolve().parent
INK, CREAM, YELLOW, PAPER, GREY = (18, 17, 16), (240, 232, 214), (253, 208, 12), (222, 212, 188), (150, 143, 122)
LINES = ('MAKE', 'HELLDIVERS')          # cream title lines
BAR = 'GREAT AGAIN'                     # dark type on the yellow bar
CAPTION = ('ONE INSTALL', 'PICK YOUR MODS')
# Mirrors the list in upstream's pack_cover.py (kept literal: that module needs Windows fonts to import).
MODS = ['BETTER STRATAGEM BOUNCE', 'HELLPOD STEERING UNLOCKED', 'REINFORCEMENT BEACONS FIXED', 'CONSISTENT VAULTING',
        'SHALLOW WATER DIVING', 'SENTRY AIM RETENTION', 'ENEMY COLLISION SYNCHRONIZED', 'CONTROLLABLE HOVER PACK',
        'KNOW YOUR CONSTELLATION', 'ARMORY PREVIEW CACHE', 'ARC THROWER REVAMPED', 'CLICKABLE SCROLLBARS',
        'SHIP STATION HOTKEYS']


def font(name, size):
    return ImageFont.truetype(str(HERE / 'fonts' / name), round(size))


def fit(draw_text, name, text, width, squeeze=1.0):
    lo, hi = 10, 700
    while hi - lo > 1:
        mid = (lo + hi) // 2
        b = font(name, mid).getbbox(text)
        if (b[2] - b[0]) * squeeze > width:
            hi = mid
        else:
            lo = mid
    return font(name, lo)


def squeezed(img, text, f, x, top, fill, squeeze):
    """Draw `text` squeezed horizontally (taller letters); (x, top) is the glyph box's top left."""
    b = f.getbbox(text)
    w, h = b[2] - b[0], b[3] - b[1]
    tmp = Image.new('L', (w, h), 0)
    ImageDraw.Draw(tmp).text((-b[0], -b[1]), text, font=f, fill=255)
    tmp = tmp.resize((round(w * squeeze), h), Image.LANCZOS)
    img.paste(Image.new('RGB', tmp.size, fill), (round(x), round(top)), tmp)
    return tmp.size


def tracked(d, xy, text, f, fill, tracking, anchor='ls'):
    x, y = xy
    widths = [f.getlength(c) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    if anchor == 'rs':
        x -= total
    for c, w in zip(text, widths):
        d.text((x, y), c, font=f, fill=fill, anchor='ls')
        x += w + tracking


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(HERE / 'thumbnail.png'))
    args = ap.parse_args()
    rng = np.random.default_rng(1984)
    arr = np.zeros((N, N, 3), float) + INK
    # paper: warm cream with soft mottling and fine grain
    top = 704
    blot = gaussian_filter(rng.standard_normal((N, N)), 38)
    blot /= blot.std()
    grain = rng.standard_normal((N, N))
    arr[top:] = np.array(PAPER, float) + (blot[top:] * 2.4 + grain[top:] * 1.5)[..., None]
    arr[:top] += (gaussian_filter(rng.standard_normal((top, N)), 1.2) * 1.4 + rng.standard_normal((top, N)) * 0.8)[..., None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB')
    d = ImageDraw.Draw(img)

    title = 'ArchivoBlack-Regular.ttf'
    sq = 0.84
    x0 = 88
    f1 = fit(d, title, LINES[0], 560, sq)
    w1, h1 = squeezed(img, LINES[0], f1, x0, 92, CREAM, sq)
    f2 = fit(d, title, LINES[1], 1010, sq)
    y2 = 92 + h1 + 30
    w2, h2 = squeezed(img, LINES[1], f2, x0, y2, CREAM, sq)
    # three slashes after the first line
    sx, sy0, sy1 = x0 + w1 + 46, 92 + int(h1 * 0.34), 92 + h1
    for i in range(3):
        a = sx + i * 36
        d.polygon([(a, sy1), (a + 16, sy1), (a + 16 + 58, sy0), (a + 58, sy0)], fill=YELLOW)
    # caption, top right
    cf = font('BarlowCondensed-SemiBold.ttf', 31)
    for i, line in enumerate(CAPTION):
        tracked(d, (1168, 112 + i * 40), line, cf, GREY, 4.5, anchor='rs')

    # yellow bar with a chamfered bottom-right corner, dark type
    by0, by1 = y2 + h2 + 40, y2 + h2 + 40 + 192
    d.polygon([(0, by0), (1167, by0), (1167, by1 - 48), (1119, by1), (0, by1)], fill=YELLOW)
    fb = fit(d, title, BAR, 1010, sq)
    bb = fb.getbbox(BAR)
    squeezed(img, BAR, fb, x0, by0 + (by1 - by0 - (bb[3] - bb[1])) / 2, INK, sq)

    # hazard band between the dark ground and the paper
    hy0, hy1, stripe = 672, 704, 17
    d.rectangle([0, hy0, N, hy1 - 1], fill=YELLOW)
    x = -(hy1 - hy0)
    while x < N:
        d.polygon([(x + 32, hy0), (x + 32 + stripe, hy0), (x + stripe, hy1), (x, hy1)], fill=INK)
        x += 2 * stripe
    # packing slip
    tracked(d, (88, 764), 'CONTENTS', font('BarlowCondensed-SemiBold.ttf', 36), INK, 5)
    tracked(d, (1168, 764), 'ENABLE ANY', font('BarlowCondensed-SemiBold.ttf', 27), INK, 4, anchor='rs')
    d.rectangle([88, 780, 1167, 783], fill=INK)
    rf = font('BarlowCondensed-SemiBold.ttf', 30)
    for i, mod in enumerate(MODS):
        col, row = i % 2, i // 2
        x, y = 88 + col * 538, 826 + row * 84
        d.rectangle([x, y - 6, x + 25, y + 19], fill=INK)
        d.line([(x + 5, y + 7), (x + 11, y + 14), (x + 21, y - 1)], fill=PAPER, width=4, joint='curve')
        tracked(d, (x + 42, y + 19), mod, rf, INK, 2.2)
    img.save(args.out, optimize=True)
    print('wrote', args.out)


if __name__ == '__main__':
    main()
