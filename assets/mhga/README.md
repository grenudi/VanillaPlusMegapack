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

Not changed: `../thumbnail.png`, the pack's box icon in Arsenal/HD2MM, still reads VANILLA PLUS / MEGAPACK.
Upstream draws it with Windows fonts (Franklin Gothic Heavy, Bahnschrift) that are not available on
non-Windows machines, so it is left as is rather than re-rendered with different type.
