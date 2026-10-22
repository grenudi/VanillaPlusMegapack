# MHGA artwork

`banner.png` (2172x724) is the README banner for **Make Helldivers Great Again (MHGA)**.

It follows the same visual direction as the upstream Vanilla Plus Megapack banner (see
[`../ARTWORK.md`](../ARTWORK.md), "Banner"): pure typography on a distressed charcoal ground, wide heavy
cream and yellow block type in two stacked lines, clipped yellow border rules that step at the right (top)
and left (bottom), three yellow hazard slashes bottom left, yellow wear in the corners and a small
letter-spaced cream footer. Palette from upstream's art system: ground `#121110`, cream `#f0e8d6`,
yellow `#fdd00c`.

Unlike upstream's banner (made with an image generator), this one is **drawn in code**, so it can be
regenerated and edited: `python banner.py` (needs Pillow, NumPy, SciPy), deterministic for a fixed seed.
The footer is `--footer "..."`; by default it credits the upstream project.

Fonts in `fonts/` are SIL Open Font License: Archivo Black (title, squeezed horizontally to 80%) and
Barlow Condensed SemiBold (footer). License texts are alongside.

## Box icon

`thumbnail.png` (1254x1254) is the pack's image in Arsenal and HD2MM, selected by `icon` in
[`../../branding.json`](../../branding.json) and packaged as `thumbnail.png`. Same layout as upstream's code-drawn
icon (`../source/pack_cover.py`): title on a dark ground, yellow bar, hazard band, then a packing slip listing the
bundled mods, running off the edge. Upstream renders it with Windows fonts (Franklin Gothic Heavy, Bahnschrift) that
are not available elsewhere, so this one is drawn by `thumbnail.py` with the OFL fonts in `fonts/`; it is a close
recreation, not a pixel match. `python thumbnail.py` regenerates it (deterministic). Upstream's own
`../thumbnail.png` is left untouched.
